#!/usr/bin/env python3
"""Test whether the presigned callback URL survives the trip through Deepgram.

The direct presigned PUT already works (200). This checks the two remaining
suspects for the callback failure:

  1. URL mangling — the presigned URL is passed as a query param to Deepgram,
     percent-encoded, then decoded again on Deepgram's side. This reproduces
     that encode -> decode round trip and confirms it reconstructs the URL
     exactly, then PUTs to the reconstructed URL.
  2. Method — a presigned PUT URL is only valid for PUT. If Deepgram ignored
     callback_method=put and used POST, S3 would reject it. This also fires a
     POST at the same URL to show that failure signature.

Run after: set -a; source .env; set +a
    python3 bin/test_callback_roundtrip.py [REGION]
"""

import os
import sys
from urllib.parse import urlencode, urlparse, parse_qs

import boto3
import requests

region = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
bucket = "ttrpg-deepgram"
key = "2026-08-11/test-callback-roundtrip.json"

s3 = boto3.client("s3", region_name=region)
put_url = s3.generate_presigned_url(
    "put_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=300)
print(f"generated presigned PUT URL (len={len(put_url)})")

# Exactly what bin/deepgram_async.py puts on the Deepgram request URL:
query = urlencode({"model": "nova-3", "callback": put_url, "callback_method": "put"})
deepgram_url = f"https://api.deepgram.com/v1/listen?{query}"

# What Deepgram's server sees after parsing the query string (one decode):
callback_seen = parse_qs(urlparse(deepgram_url).query)["callback"][0]
print("round-trip reproduces the URL exactly:", callback_seen == put_url)

# (1) PUT to the round-tripped URL, as Deepgram should when callback_method=put:
r_put = requests.put(callback_seen, data=b'{"roundtrip": true}')
print(f"PUT  -> HTTP {r_put.status_code}  {r_put.text[:300] or '(empty = success)'}")

# (2) POST to the same URL, as Deepgram would if callback_method were ignored:
r_post = requests.post(callback_seen, data=b'{"roundtrip": true}')
print(f"POST -> HTTP {r_post.status_code}  {r_post.text[:300] or '(empty = success)'}")

#!/usr/bin/env python3
"""Reproduce Deepgram's callback: a presigned PUT straight to S3.

This isolates the exact operation Deepgram performs when it delivers the result
(a PUT to a presigned URL) so we can see S3's real error, without Deepgram in the
path. Run it after loading AWS creds (set -a; source .env; set +a).

Usage:
    python3 bin/test_s3_put.py [REGION] [BUCKET]

REGION must be the region the bucket actually lives in (S3 console shows it next
to the bucket name). Defaults: region from AWS_DEFAULT_REGION or us-east-1,
bucket ttrpg-deepgram.
"""

import os
import sys

import boto3
import requests

region = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
bucket = sys.argv[2] if len(sys.argv) > 2 else "ttrpg-deepgram"
key = "2026-08-11/test-put.json"

print(f"region={region}  bucket={bucket}  key={key}")

s3 = boto3.client("s3", region_name=region)
url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": bucket, "Key": key},
    ExpiresIn=300,
)

resp = requests.put(url, data=b'{"ok": true}')
print("HTTP", resp.status_code)
print(resp.text[:800] or "(empty body = success — the presigned PUT works)")

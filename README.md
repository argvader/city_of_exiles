# City of Exiles

Session archive and campaign wiki for **City of Exiles** — a Dungeons & Dragons
5th Edition campaign set in the world of **Erratt**, beginning in **Utsa
Paradisa**, the City of Exiles.

The site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
and published to GitHub Pages.

- **`docs/`** — the published site (sessions + wiki). Built by MkDocs.
- **`sessions-raw/`** — raw inputs per session (transcripts, notes). Not published.
- **`SESSION_SUMMARIZER.md`** — the prompt used to turn raw materials into the site.
- **`WORLD.md`** — the Erratt campaign bible (setting reference).

---

## The Process

```
OBS (record audio) → Deepgram (transcribe + diarize) → format transcript
   → sessions-raw/<DATE>/ → run SESSION_SUMMARIZER.md → commit → GitHub Pages
```

### 1. Record the audio (OBS Studio)

1. In OBS, open **Settings → Audio** and make sure your sources are captured:
   - **Mic/Aux** — your microphone (the DM).
   - **Desktop Audio** — the remote players coming through your voice app
     (Discord/etc.).
2. *(Recommended for cleaner speaker separation)* Enable multi-track recording:
   **Settings → Output → Output Mode: Advanced → Recording → Audio Track**, and
   assign each source to its own track. Use the **`.mkv`** container so multiple
   tracks are preserved (remux to `.mp4` later if needed).
3. Click **Start Recording** before play, **Stop Recording** after.
4. Find the file under your configured **Recording Path**.

> Deepgram accepts common audio/video formats (`wav`, `flac`, `mp3`, `m4a`,
> `mkv`, `mp4`, …), so you can usually upload the OBS file directly. If you
> recorded multi-track and want a single mix, export/remux to a `.wav` first.

### 2. Transcribe with Deepgram (diarization on)

Send the recording to Deepgram with **diarization** and **utterances** enabled.
Diarization separates speakers (Speaker 0, Speaker 1, …); utterances give you
timestamped, speaker-tagged segments that map cleanly to the transcript format.

```bash
curl --request POST \
  --url 'https://api.deepgram.com/v1/listen?model=nova-3&diarize=true&punctuate=true&smart_format=true&utterances=true' \
  --header "Authorization: Token $DEEPGRAM_API_KEY" \
  --header 'Content-Type: audio/wav' \
  --data-binary @session.wav \
  > session.deepgram.json
```

> If you recorded **multi-track** (one track per speaker), you can instead
> transcribe each track separately *without* diarization — the speaker is known
> per track — and merge by timestamp. Diarization on a single mix is the simpler
> default.

### 3. Format the transcript

Convert Deepgram's `utterances` into the `transcript.md` format the summarizer
expects: a per-line `MM:SS <Player> as <Character>:` (or `<Player> the DM:` for
the DM), e.g.

```text
00:00 Ian the DM: The little boy crept into the silver shop...
00:15 Ian the DM: In the interrogation you learn he was being paid by the ruling family.
01:58 Matt as Krum: Wait — how much money are we talking?
02:01 Ian the DM: A pretty good sum.
```

Speaker labels for this campaign:

| Deepgram speaker | Label to use            |
|------------------|-------------------------|
| (the DM's voice) | `Ian the DM`            |
| Josh             | `Josh as Adarius`       |
| Jonathan         | `Jonathan as Behnsun Payne` |
| Kevin            | `Kevin as Fizz`         |
| Matt             | `Matt as Krum`          |
| Gary             | `Gary as Prance Galavant` |

Deepgram assigns speaker **numbers**, not names, and the numbering changes per
recording — so listen to a few lines once to learn which number is whom, then
build the mapping. This `jq` one-liner formats the JSON and substitutes names in
one pass (edit the `map` to match this recording's speaker numbers):

```bash
jq -r --argjson map '{
  "0":"Ian the DM",
  "1":"Josh as Adarius",
  "2":"Jonathan as Behnsun Payne",
  "3":"Kevin as Fizz",
  "4":"Matt as Krum",
  "5":"Gary as Prance Galavant"
}' '
  def p2: tostring | if length < 2 then "0" + . else . end;
  .results.utterances[]
  | (.start|floor) as $t
  | "\(($t/60|floor)|p2):\(($t%60)|p2) \($map[(.speaker|tostring)] // "Speaker \(.speaker)"): \(.transcript)"
' session.deepgram.json > transcript.md
```

### 4. Drop the materials into `sessions-raw/<DATE>/`

```
sessions-raw/2026-06-04/
  transcript.md       # required — formatted above
  dm-notes.md         # optional — GM prep / notes
  <player>-notes.md   # optional — e.g. matt-notes.md
```

The summarizer treats the **newest** date folder as the latest session.

### 5. Generate the site content

Run the prompt in [`SESSION_SUMMARIZER.md`](SESSION_SUMMARIZER.md). It reads the
newest `sessions-raw/<DATE>/`, the existing `docs/`, and `WORLD.md`, then:

- updates/creates wiki entries under `docs/wiki/{pcs,npcs,factions,locations}/`,
- writes the session summary to `docs/sessions/<DATE>.md`,
- updates the nav in `mkdocs.yml` and the table in `docs/index.md`.

### 6. Preview locally (optional)

```bash
pip install mkdocs-material
mkdocs serve     # http://127.0.0.1:8000
```

### 7. Publish

Commit and push to **`main`**. The
[`deploy-docs`](.github/workflows/deploy-docs.yml) GitHub Action runs
`mkdocs gh-deploy --force`, building the site and publishing it to the
**`gh-pages`** branch at
<https://argvader.github.io/city_of_exiles/>.

```bash
git add docs mkdocs.yml
git commit -m "publish session <DATE>"
git push origin main
```

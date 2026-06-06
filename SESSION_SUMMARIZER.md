# Session Summarizer — City of Exiles

## Task Description

This is the session summarizer for **City of Exiles**, a
**Dungeons & Dragons 5th Edition** campaign.
We play remotely and capture audio with OBS Studio, then transcribe with
Deepgram (diarization on) to get per-speaker transcripts.

I will provide:

- Previous session summaries (if available)
- The wiki with PC, NPC, faction, and location entries
- Raw materials from the latest session (transcript, DM notes, player notes)

Using the provided information, generate the following outputs in **Markdown**,
formatted for MkDocs Material.

---

## Output Required

### 1. Wiki Updates

Update or create entries in `docs/wiki/` organized by category:

#### Player Characters (`docs/wiki/pcs/`)
Update existing PC files with new information from this session — abilities used,
character development, relationships formed.

#### NPCs (`docs/wiki/npcs/`)
For each NPC encountered (new or returning), create or update their file:

- **Name and role** (title, occupation, affiliation)
- **Appearance** and distinguishing traits
- **Personality** and behavior observed
- **Goals and motivations** (known or inferred)
- **Relationships** with PCs and other NPCs
- **Session history** — key interactions and developments

#### Factions (`docs/wiki/factions/`)
Update faction entries with new information about:
- Leadership and membership changes
- Goals and current activities
- Relationship changes with the party or other factions

#### Locations (`docs/wiki/locations/`)
For significant locations visited or mentioned:
- Description and notable features
- Who/what can be found there
- Events that occurred there

---

### 2. Session Summary

Create a session summary file in `docs/sessions/` named by date
(e.g., `2026-06-04.md`).

Structure as follows:

#### Overview
A 2-3 sentence summary of what happened this session.

#### Key Events
Detailed bullet points covering:
- Major decisions and their consequences
- Combat encounters and outcomes
- Discoveries (lore, secrets, items, clues)
- Significant character moments and roleplay

#### Memorable Moments
Highlight standout moments worth remembering:
- Creative problem-solving
- Great roleplay or dramatic scenes
- Exceptional bravery, skill, or resourcefulness
- Funny, unexpected, or cinematic moments

#### Open Threads
- Unresolved plot points and mysteries
- Promises made or debts owed
- Suggested next steps and story hooks

#### Dramatized Scene (Interactive)

After completing the summary, **suggest 3-5 scenes** from the session that could
be dramatized as short prose. For each suggestion, provide:
- A short title
- A one-sentence description of the moment

**Wait for the user to choose one.** Then write a **3-paragraph dramatization**
of that scene — vivid, atmospheric prose that brings the moment to life. Include
sensory details, character voice, and tension.

Add the dramatized scene to the session summary under a `## The Scene` heading,
placed **at the very end** of the file (after the Timeline section).

---

### 3. Navigation Update

Add the new session to `mkdocs.yml` under the `Sessions:` nav entry.

Example — if the session is `2026-06-18.md` (Session Two), add:

```yaml
nav:
  - Sessions:
      - "Session One (2026-06-04)": sessions/2026-06-04.md
      - "Session Two (2026-06-18)": sessions/2026-06-18.md   # ← add new session here
```

Include the date in parentheses after the session name. Use a descriptive title
like "Session One", "Session Two", etc., or a thematic title if the session had a
clear narrative arc (e.g., "Whispers in the Archives").

Also add new wiki pages to the `Wiki:` nav entry under their category, and add the
session row to the table in `docs/index.md`.

---

### 4. Cross-Linking

Use standard Markdown links to connect content:

- **Session files** → Link NPC names on first mention:
  `[The Enigmatic Ally](../wiki/npcs/the-enigmatic-ally.md)`
- **NPC files** → Cross-reference other NPCs, factions, and locations
- **Location files** → Link to NPCs found there and events that occurred

**Do NOT link PCs** — they appear too frequently and would create excessive links.

Use relative paths from the file's location. Keep link text natural:
`[the Ally](../wiki/npcs/the-enigmatic-ally.md)` reads better than the full title.

---

## Input Sources

### World Bible
`WORLD.md` (repo root) — the canonical setting reference for Erratt: nations,
races, factions, geography, and pantheon. Use it to keep names, places, and lore
consistent, and to place new NPCs/locations correctly in the world.

### Previous Sessions
Located in `docs/sessions/` — read for context and continuity.

### Wiki
Located in `docs/wiki/` — reference for existing characters, factions, and locations.

### Latest Session Materials
Located in `sessions-raw/[DATE]/`:
- `transcript.md` — Full session transcript
- `dm-notes.md` — GM's session notes and prep
- `*-notes.md` — Individual player notes (e.g., `braedon-notes.md`)

Find the newest date folder for the latest session.

### Participants

**Ian** is the **Dungeon Master** — he is not a player, but his voice appears as
a speaker in the transcript (he voices all NPCs and narration).

| Player | Character        | Ancestry | Class    |
|--------|------------------|----------|----------|
| Josh   | Adarius          | Human    | Wizard   |
| Jonathan | Behnsun Payne  | Human    | Sorcerer |
| Kevin  | Fizz             | Myconid  | Bard     |
| Matt   | Krum             | Dwarf    | Rogue    |
| Gary   | Prance Galavant  | Harengon | Paladin  |

---

## Setting Context

The campaign is set in the world of **Erratt**, shaped by **the Schism** — a
cataclysm in which the Feywild tried to merge with the material plane, spilling
out magic and Fey, splitting the land, and awakening the Beastfolk. Its
aftermath defines every nation's borders, grudges, and alliances. See
[`WORLD.md`](WORLD.md) for the full campaign bible (nations, races, pantheon).

The party begins in **Utsa Paradisa — "the City of Exiles"**, a desert oasis in
the Northern Territories:

- **Water is sacred and scarce** — heavily guarded; control of it is power.
- **A haven for the exiled** — predominantly Tieflings shunned by long-dead
  nations, plus a large Tabaxi population and other exiled beastfolk; the
  disenfranchised of Erratt end up here.
- **Empress Selene** of Utsa Paradisa brokered the tenuous peace between
  Drathomir and the Goliaths, so the city carries real diplomatic weight.
- **Trade lifeline** — close partnership with **UkRuundir** (Goliath capital),
  trading tar and spices for lumber and mammoth meat across a brutal
  desert-to-cold-forest crossing.
- **Tone** — exiles and outcasts carving out belonging amid prejudice, scarcity,
  and the long shadow of the Schism.

Key powers in the wider world: the three great nations of **Trivan**, the **Iron
Holds**, **Drathomir**, and **Medui-Ghislerin** (the Tree of Five Families), with
the **Riverlands**/**Emerald Wilderness** and the Northern Territories beyond.

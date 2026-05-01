# Music library

## TL;DR

`Artist/Year - Album/NN Track Name.flac` is the de-facto layout for a self-hosted music collection. The artist directory groups everything by performer; the year-prefixed album directory sorts releases chronologically without needing a tag query; the two-digit track-number prefix sorts songs in playback order in any file browser. This is what Beets emits by default, what MusicBrainz Picard's stock script targets, and what Plex, Jellyfin, Roon, and Navidrome all recognise without configuration. Spaces are intentional — directory names match the human-readable metadata, which is what users see in their players. Audio tags (FLAC Vorbis comments, ID3 in MP3) remain the source of truth; filenames mirror the tags so the layout survives if a tag library gets corrupted.

## Principles & why

A library scales by metadata, not directory shape. Every modern music player reads tags first; the on-disk path exists to make the collection navigable when the indexer is offline or to bootstrap a freshly installed player. The layout encodes three retrieval modes that a path alone can answer without an index:

1. **By artist** — top-level directories list every performer alphabetically; the eye lands on `Radiohead/` instantly.
2. **By release order** — inside an artist, `1997 - OK Computer/` sorts before `2000 - Kid A/`. No tag lookup needed.
3. **By track order** — inside an album, `01 Airbag.flac` sorts before `02 Paranoid Android.flac`. Drag-and-drop into any device or playlist preserves album order.

The two-digit zero-padded track number is non-negotiable: without padding, `10` sorts before `2` in lexicographic order, scrambling the album. The year-dash-album form lets you eyeball discography breadth without opening any player. And keeping artist as the root means compilations and "Various Artists" releases live in their own well-known bucket rather than polluting individual artist directories.

## When to use

- Self-hosted music libraries served by Plex, Jellyfin, Emby, Navidrome, Subsonic, Airsonic, or Roon — every one of these recognises this layout out of the box.
- Beets-managed collections — `beet import` defaults to a path template that emits exactly this shape (`$albumartist/$year - $album/$track $title`).
- MusicBrainz Picard users — the official "Plex/Jellyfin compatible" preset writes this layout.
- FLAC/ALAC archive collections where lossless masters need to coexist with transcoded lossy copies (mirror the tree under `Music-mp3/` for a perfect parallel).
- DJ rip libraries shared between desktop tools (Mixxx, Rekordbox export folders) — the layout is generic enough that every tool reads it without reorganising.

## When NOT to use

- Streaming-only setups (Spotify, Apple Music, Tidal, YouTube Music) — there is no local library to organise; the platform owns the catalogue.
- Classical music collections — the artist-first scheme breaks down because you search by composer, conductor, soloist, or ensemble depending on the work. Use a `Composer/Work - Performer (Year)/` variant instead, or a tag-driven DAM like Roon's classical-aware mode.
- Live-recording archives where every show is its own release — the year/album hierarchy doesn't model `2024-04-15 Madison Square Garden/` cleanly. Use date-rooted: `Artist/YYYY-MM-DD Venue/`.
- DJ working sets — DJ tools (Rekordbox, Serato, Traktor) maintain their own database that shouldn't be reshuffled by a path-driven library tool.
- Mobile devices — phone music apps usually flatten anything you side-load. The layout is preserved on device but does no work there.

## Tree diagram

```
Music/
├── Radiohead/
│   ├── 1997 - OK Computer/
│   │   ├── 01 Airbag.flac
│   │   ├── 02 Paranoid Android.flac
│   │   └── cover.jpg
│   └── 2000 - Kid A/
│       ├── 01 Everything in Its Right Place.flac
│       └── cover.jpg
└── Various Artists/
    └── 2020 - Compilation Title/
```

## Naming rules

1. The top-level is the library root, conventionally `Music/` or `Audio/`. Use a consistent name across machines so paths are portable.
2. Artist directories use the album-artist field (not the per-track artist) so featured artists don't fork the discography. `Radiohead/` not `Radiohead feat. Bjork/`.
3. Album directories carry the four-digit release year, a space-dash-space separator, and the title: `1997 - OK Computer/`. The year is the original-release year, not the reissue year, so the chronology stays accurate.
4. Track filenames are `NN Title.ext` — two-digit zero-padded track number, single space, title, dot-extension. Multi-disc albums use `D-NN` (e.g. `1-01`, `1-02`, `2-01`).
5. Compilations and split releases live under `Various Artists/`. The album-artist tag must be set to "Various Artists" for this to work; players use that tag to suppress the per-track artist confusion.
6. Album-art lives in the album directory as `cover.jpg` or `folder.jpg` (Windows convention). Most players check both. Embedded art in the audio tag still wins for portability.
7. Spaces in directory and file names are intentional and match human-readable metadata. Quote paths in shell scripts; never substitute hyphens or underscores for spaces.

## Anti-patterns

- **One-digit track numbers** — `1 Airbag.flac, 2 Paranoid Android.flac, ..., 10 Lucky.flac` sorts as `1, 10, 2, 3, ...`, scrambling the album.
- **Album directory without year** — `Radiohead/OK Computer/` works but loses chronology; you can't see at a glance which album came first without opening tags.
- **Featured-artist forks** — separating `Beyonce - Cuff It/` from `Beyonce feat. Jay-Z - Cuff It/` produces two directories for the same artist; use album-artist tag.
- **Embedding genre in the path** — `Rock/Radiohead/...` and `Electronic/Radiohead/...` causes Radiohead to appear twice; let players group by the genre tag instead.
- **Renaming files to match a service-specific scheme** — Apple's `01 Airbag.m4a` and Spotify's per-track URI schemes diverge from this; pick one and stick with it.
- **Storing playlists inside album directories** — `.m3u` files belong in a sibling `Playlists/` directory, not inside `OK Computer/`.
- **Letting cloud sync rewrite filenames** — some sync clients normalise Unicode forms (NFC vs NFD) and cause duplicates; pick a consistent form on import.

## Variants

- **With disc numbers** — `D-NN Track.flac` (e.g. `1-01 Track.flac`, `2-05 Track.flac`) for multi-disc releases. Beets emits this when the album has more than one disc.
- **With genre prefix** — `Rock/Radiohead/...`. Some users want filesystem-level genre browsing; the tradeoff is artist duplication when genres overlap.
- **Classical** — `Composer/Work - Performer (Year)/` rooted on composer. A separate guide in this collection should cover classical layouts when added.
- **Catalogue-rooted** — `Catalogue/<label>/<release>/` for collectors who think in label catalogue numbers (Blue Note, ECM). Niche but well-defined.
- **MusicBrainz-rooted** — uses MusicBrainz release IDs in the path for unambiguous identity. Beets supports this with `albumtype:%aunique{}` placeholders.
- **Year-first** — `2026/Radiohead - Album/...`. Useful for chronological listening parties; useless for daily artist-based browsing.

## Real-world projects using this

- **Beets** — the dominant CLI music tagger. Default path template is `$albumartist/$year - $album%aunique{}/$track $title` which produces exactly this layout.
- **MusicBrainz Picard** — official tagging client; ships a "Plex/Jellyfin/Roon compatible" preset script that emits this shape.
- **Plex Media Server** — "Personal Media" music libraries are documented as `Music/Artist/Album/Track.ext` and tolerate the year prefix on the album directory.
- **Jellyfin** — music library docs specify the same layout with optional year on the album.
- **Roon** — library import guidelines explicitly reference this scheme.
- **Navidrome** — Subsonic-compatible self-hosted server; reads this layout natively.
- **Lidarr** — Sonarr/Radarr's music sibling; default rename templates produce `{Artist Name}/{Year} - {Album Title}/{track:00} - {Track Title}.{ext}`.

## Migration & references

To enforce this layout on a flat or inconsistent library, drive the rename from tags using Beets:

```bash
# beet config.yaml fragment
directory: ~/Music
paths:
    default: $albumartist/$year - $album%aunique{}/$track $title
    singleton: Non-Album/$artist/$title
    comp: Various Artists/$year - $album%aunique{}/$track $title
```

```bash
# bulk import an existing library, applying tags from MusicBrainz
beet import -A path/to/library
# then move files to the canonical layout
beet move
```

For non-Beets users, MusicBrainz Picard's Tools menu has a "Move to" feature that uses its scripting language to emit identical paths.

Further reading:

- Beets documentation — https://beets.readthedocs.io/
- MusicBrainz Picard documentation — https://picard-docs.musicbrainz.org/
- Plex naming guide for personal media (music section) — https://support.plex.tv/articles/200265296/
- Jellyfin music library documentation — https://jellyfin.org/docs/general/server/media/music/
- `principles/iso-date-formats/` — the year-prefix pattern this layout uses.
- `principles/naming-by-purpose-not-type/` — why `Artist/` beats `Audio/` as a top-level grouping.
- `files/video-library/` — the sibling layout for Plex/Jellyfin movies and TV.

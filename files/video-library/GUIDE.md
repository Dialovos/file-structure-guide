# Video library

## TL;DR

Plex's "Personal Media" naming convention has become the de-facto standard for self-hosted video libraries: `Movies/Title (Year)/Title (Year).ext` for films, `TV Shows/Show Name/Season XX/Show Name - sXXeYY.ext` for episodic content. The year disambiguates remakes and same-title coincidences (`Dune (1984)` vs `Dune (2021)`); the per-show season-folder layout matches how scrapers — Plex's, Jellyfin's, Sonarr's, Radarr's — emit metadata sidecars and how renamers like FileBot expect to land files. Strict adherence is what unlocks automatic metadata, posters, and chapter art; loose layouts produce silent matching failures that look like the server is broken.

## Principles & why

A media server is a metadata problem dressed up as a file-serving problem. Every modern video server (Plex, Jellyfin, Emby) parses the path to derive an identity, then queries TheMovieDB, TheTVDB, or AniDB for metadata. The path needs to encode three independent facts unambiguously:

1. **Type** — movie or TV. The top-level `Movies/` vs `TV Shows/` directory separates the matchers; mixing types breaks both.
2. **Identity** — the title and year (for movies) or the show name (for TV). Year goes in parentheses because every scraper recognises that as the disambiguator.
3. **Position in series** — for TV, season and episode. The `sXXeYY` convention is universal: lowercase `s` and `e`, two-digit zero-padded numbers, no separator between season and episode.

Why two-digit padding matters: a 13-episode season files `s01e10` after `s01e09` and before `s01e11` only if the digits are zero-padded; otherwise `s01e10` sorts before `s01e2`. Why year in parens for movies: scrapers regex `(\d{4})` from the parens — bare years get confused with edition numbers (`Blade Runner 2049 (2017)` is title `Blade Runner 2049`, year `2017`, not title `Blade Runner` year `2049`).

## When to use

- Plex, Jellyfin, Emby, or Kodi libraries — every one of these recognises this layout natively and matches metadata without configuration.
- Sonarr/Radarr-managed downloads — these tools emit exactly this layout when their default rename templates are kept.
- FileBot and tinyMediaManager users — both ship presets that produce this layout.
- Mixed libraries that you intend to share with other media-server tools later — the layout is the lingua franca; switching backends is painless.
- Multi-user households where a partner or kids browse via a smart-TV Plex/Jellyfin app — the path shape is invisible to them but enables the polished UI.

## When NOT to use

- Personal home videos and family camcorder footage — those should live in the photo-library scheme (`files/photos-by-date-and-event/` extended with video extensions); they have no canonical title or year.
- Educational courses (Coursera, Udemy, conference talks) — use a `Course Name/01-Module/01-lesson-title.mp4` scheme; the season/episode shoehorn is misleading.
- Raw camera-card dumps awaiting edit — those go in a project working tree under `files/project-archive/`.
- Anime collections that use absolute episode numbering — anime needs `Show Name - eNNN.ext` or AniDB-aligned `[Group] Show - 01.mkv`; the season/episode form misrepresents the series.
- Cinema-grade DCP packages — these have their own structure (`<MediaTitle>_<Encoding>_<Language>_<Date>_<Studio>_..._SMPTE.dcp/`) that this layout doesn't replace.

## Tree diagram

```
Video/
├── Movies/
│   ├── Inception (2010)/
│   │   ├── Inception (2010).mkv
│   │   └── poster.jpg
│   └── Arrival (2016)/
│       └── Arrival (2016).mkv
└── TV Shows/
    └── Severance/
        ├── Season 01/
        │   ├── Severance - s01e01.mkv
        │   └── Severance - s01e02.mkv
        └── Season 02/
```

## Naming rules

1. Top-level split is always `Movies/` and `TV Shows/`. Do not mix; the matchers refuse to recognise a film inside a TV directory and vice versa.
2. Movie directory and file: `Title (Year)/Title (Year).ext`. The year goes in parentheses. The directory and the file repeat the same name; this redundancy lets Plex's chapter-thumbnail and trailer-sidecar features work.
3. TV show root: `Show Name/`. No year unless two shows share a title (`Doctor Who (1963)/` vs `Doctor Who (2005)/`).
4. Season directory: `Season XX/` — zero-padded two-digit. Plex also accepts `Season 1/` but `Season 01/` sorts correctly past nine.
5. Episode file: `Show Name - sXXeYY.ext`. Lowercase `s` and `e`. Two-digit zero-padded numbers. Optional title hint after: `Severance - s01e01 - Good News About Hell.mkv`.
6. Multi-episode files: `Show Name - sXXeYY-eZZ.ext` for double-headers (e.g. `s01e01-e02`).
7. Specials and pilots: `Season 00/` for pre-season specials; episode `s00e01` for the pilot if it's not part of a numbered season.
8. Sidecar files (subtitles, posters, NFOs) sit next to the media file with matching base names: `Inception (2010).en.srt`, `Severance - s01e01.en.srt`. Posters as `poster.jpg`, banners as `banner.jpg`.

## Worked example

Movies and shows are scattered as `Movie.2010.1080p.x264.mkv` and `S01E01 - Pilot.mkv`, and the media server shows wrong matches.

1. Create `Movies/` and `TV Shows/` at the library root.
2. Rename each film into its own folder: `Movies/Inception (2010)/Inception (2010).mkv`. The year disambiguates remakes.
3. For shows: `TV Shows/Severance/Season 01/Severance - s01e01.mkv`. Season folders are `Season 01`, `Season 02`, and specials go in `Season 00`.
4. Keep extras and subtitles beside the file with matching names: `Inception (2010).en.srt`, `poster.jpg`.
5. Add the library to Plex or Jellyfin and check the "unmatched" list; fix names, not the metadata, whenever possible.
6. Automate renaming with `filebot` or the *arr tools if the volume is high.

The server identifies every title on the first scan.

## Anti-patterns

- **No year on movie directory** — `Movies/Dune/Dune.mkv` matches the wrong remake half the time. Always add `(Year)`.
- **Year without parentheses** — `Movies/Dune 2021/` confuses scrapers; the regex looks for `(\d{4})` in parens.
- **Single-digit season or episode numbers** — `Season 1/` and `s1e1.mkv` work, but break sort order past nine episodes.
- **Putting episodes in the show root without season directories** — `Show Name/s01e01.mkv` sometimes matches but most scrapers want the season directory.
- **Renaming files without renaming the directory** — Plex matches the directory first; a directory called `Random Movie Folder/` with `Inception (2010).mkv` inside often fails to match.
- **Mixing types** — a `TV Shows/Severance/Severance Movie (2026).mkv` standalone file confuses the TV scraper; it goes in `Movies/`.
- **Storing extras inside season directories** — `Season 01/Behind the Scenes.mp4` triggers a "missing s01e02" warning. Plex's convention is a `Featurettes/` or `Extras/` sibling directory.
- **Spaces vs dots in episode filenames** — `Show.Name.s01e01.mkv` works in some renamers but Plex docs prefer spaces and a dash separator.

## Scaling & failure modes

- **Split editions and multiple versions** need the server's naming for versions (`Movie (2010) - 4K.mkv`); check the server docs.
- **Anime and daily shows** use different numbering (absolute or date-based); follow the specific scraper's guidance.
- **Storage growth** is dominated by a few large files; plan capacity and consider transcoding rules.
- **Hardlinks with download clients** save space when a download folder and library share a filesystem; keep them on the same volume.

## Variants

- **Plex-strict** — exactly the form documented above; safest baseline.
- **Jellyfin-strict** — accepts the same shape but also tolerates `Show - S01E01 - Title.ext` (uppercase, no dash before season). Pick one form per library.
- **Kodi (XBMC)** — uses `tvshow.nfo`, `movie.nfo`, and `season-all.nfo` sidecars for metadata override; the directory shape is identical to Plex.
- **Emby** — same shape; differs only in the sidecar naming for trailers and themes.
- **Per-quality variants** — some users keep a parallel `Movies-4K/` tree for HDR rips. Plex supports multiple library roots pointing at parallel trees.
- **Year-grouped movies** — `Movies/2010/Inception (2010)/...`. Aids backups but loses Plex's poster-wall flow; uncommon.
- **Anime-specific** — `Anime/Show Name/Show Name - 01.mkv` (absolute numbering, no season). Treat as a separate library so the matcher pulls from AniDB/AniList instead of TheTVDB.

## Adoption checklist

- [ ] Every movie is in `Title (Year)/`, every episode is in `Show/Season XX/`.
- [ ] Subtitles and artwork share the base name of their video.
- [ ] The media server's unmatched list is empty.
- [ ] The download folder and library sit on the same filesystem if using hardlinks.
- [ ] A backup or replacement plan exists for irreplaceable items.

## Real-world projects using this

- **Plex Media Server** — the canonical naming source; their support article on Personal Media is the original reference for this layout.
- **Jellyfin** — open-source Plex alternative; the media-organisation docs describe an essentially identical layout.
- **Emby Server** — Plex's older sibling; same layout, different sidecar conventions.
- **Kodi (XBMC)** — accepts this layout when the library scrapers are TheMovieDB Helper / TheTVDB scraper.
- **FileBot** — the dominant cross-platform TV/movie renamer; ships presets producing exactly this layout.
- **tinyMediaManager** — Java-based metadata manager; renames into this scheme by default.
- **Sonarr / Radarr** — automation tools for TV/movies; default naming presets emit Plex/Jellyfin-compatible paths.
- **Bazarr** — companion to Sonarr/Radarr for subtitles; expects this directory shape to drop `.srt` files alongside media.

## Migration & references

To rename an existing flat library, drive from a metadata source via FileBot:

```bash
# FileBot CLI: rename movies in-place using TheMovieDB
filebot -rename -r ~/Videos/old-movies/ \
        --db TheMovieDB \
        --format "Movies/{n} ({y})/{n} ({y})"

# Rename TV episodes
filebot -rename -r ~/Videos/old-tv/ \
        --db TheTVDB \
        --format "TV Shows/{n}/Season {s.pad(2)}/{n} - {s00e00}"
```

For Sonarr/Radarr-managed libraries, set the rename template under Settings → Media Management:

```
Movies (Radarr): {Movie Title} ({Release Year})
TV (Sonarr):     {Series Title} - S{season:00}E{episode:00}
```

Further reading:

- Plex naming guide for movies — https://support.plex.tv/articles/200381043/
- Plex naming guide for TV shows — https://support.plex.tv/articles/200220687/
- Jellyfin movie organisation — https://jellyfin.org/docs/general/server/media/movies/
- Jellyfin TV organisation — https://jellyfin.org/docs/general/server/media/shows/
- TRaSH Guides (Sonarr/Radarr opinionated defaults) — https://trash-guides.info/
- `files/music-library/` — the audio sibling layout.
- `files/photos-by-date-and-event/` — the layout for home video, distinct from this scheme.

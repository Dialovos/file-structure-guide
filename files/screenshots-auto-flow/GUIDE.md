# Screenshots auto-flow

## TL;DR

Reconfigure your OS to save every screenshot into `~/Pictures/Screenshots/inbox/` with an ISO-timestamped filename (`2026-04-30T14-22-08.png`). That directory is a *holding pen*, not an archive. Once a week, you triage: keepers move into `reference/<purpose>/` subdirectories with descriptive names; everything else gets deleted. Long-term keepers eventually migrate into `archive/YYYY-MM/`. The flow has three states — *captured*, *triaged*, *archived* — and a screenshot is in exactly one of them. Without the inbox-and-triage discipline, screenshots metastasise: you'll have 4,000 unsorted PNGs by year three, none of them findable, none of them deletable because you can't tell which ones matter.

## Principles & why

The fundamental problem with screenshots is that capturing one is *trivially cheap* — `Cmd+Shift+4`, `Win+Shift+S`, two seconds — but deciding what to do with one is *not* cheap, because it requires looking at the image and remembering why you took it. The whole layout is built around that asymmetry.

Three insights drive the design:

1. **The OS is going to save the file somewhere.** You cannot prevent the capture. So the first decision is *where* the OS dumps the file. Defaulting to `~/Desktop/` (macOS factory default) or `~/Pictures/` (Windows) is wrong because both are heavily-trafficked locations where the screenshot pollutes your visual workspace. Redirecting to `~/Pictures/Screenshots/inbox/` makes the capture invisible by default — you actively go look there only when triaging.

2. **Triage is a scheduled task, not an interrupt.** Trying to file each screenshot the moment you take it kills the speed-of-capture; you'll stop taking screenshots, or worse, you'll start deferring the file decision to "later" and that screenshot lives on the Desktop forever. Putting all screenshots in one inbox and doing a weekly triage pass converts twenty 5-second decisions into one 5-minute pass, which is faster *and* makes batch-delete trivial.

3. **Most screenshots are disposable.** A typical "I'll screenshot this for reference" capture is useful for about 24 hours. By week's end, you don't remember why you took 80% of them. The triage flow is biased toward *delete*: anything you can't immediately label gets deleted. The keepers — the 20% — are the ones worth filing properly.

The directory split is between *purpose* (`reference/api-design-snippets/`) and *time* (`archive/2026-04/`). Reference is for screenshots you actively consult; archive is for screenshots you might want again later but don't currently use. When a `reference/` subdirectory hasn't been opened in six months, it migrates to `archive/`.

## When to use

- Anyone who takes more than 5 screenshots per week — the volume that defeats ad-hoc filing.
- Designers, developers, and writers collecting visual reference material — UI patterns, error messages, code snippets, charts.
- Bug reporters and QA engineers who screenshot reproductions and need to find one again next month.
- Anyone whose Desktop has more than 3 screenshot files visible right now — that's the symptom; this guide is the cure.
- Combined with `defaults write com.apple.screencapture location ~/Pictures/Screenshots/inbox` on macOS, or Windows' custom save path setting in `Settings > System > Storage > Advanced storage settings > Where new content is saved`, or Flameshot/ShareX/Greenshot's per-shortcut save paths.
- Households or shared workstations where multiple users want their screenshots quarantined per user.

## When NOT to use

- You don't keep screenshots — fine, just delete the inbox weekly with a cron job and skip the rest of this guide.
- You use a screenshot SaaS (CleanShot Cloud, Droplr, Imgur) where the canonical copy lives in the cloud and your local file is a thumbnail or expires automatically.
- Your screenshots feed a documentation pipeline directly — they belong with the docs they illustrate, not in a generic screenshot archive.
- Single-purpose capture tools where each screenshot already has a destination (e.g., a Loom-style annotation tool that uploads on capture).
- You're on a tablet or phone where the OS owns the screenshot lifecycle — Apple Photos, Google Photos, and Samsung Gallery already do their own version of this and you shouldn't fight the OS.
- You take screenshots for ephemeral chat use only (Slack, Discord, iMessage) — those auto-delete after sending; no archive needed.

## Tree diagram

```
~/Pictures/Screenshots/
├── inbox/                          ← OS-saved here (configure default)
│   └── 2026-04-30T14-22-08.png
├── reference/
│   ├── api-design-snippets/
│   └── ui-inspiration/
└── archive/
    └── 2026-04/
```

## Naming rules

1. Top-level is `~/Pictures/Screenshots/` (Linux/macOS) or `%USERPROFILE%\Pictures\Screenshots\` (Windows). Single root, three subdirectories.
2. Inbox filenames are ISO 8601 timestamps with colons replaced by dashes: `YYYY-MM-DDTHH-MM-SS.png`. Colons would conflict with Windows filesystems and confuse some shells. The `T` separates date from time, matching ISO 8601's basic-form convention.
3. The OS does this automatically once configured — don't fight the OS-generated name; just point it at `inbox/`.
4. Reference subdirectory names are kebab-case purpose slugs: `api-design-snippets/`, `ui-inspiration/`, `error-messages-prod/`. Each subdirectory is *one purpose* — when you find yourself wanting to put a screenshot in two places, that's a sign the subdirectory boundary is wrong.
5. After triage, screenshots inside `reference/<purpose>/` keep the original ISO timestamp filename — don't rename. The timestamp is provenance and chronological context. Add a description file (`reference/api-design-snippets/NOTES.md`) for context if needed.
6. Archive subdirectory names are `YYYY-MM/` matching the rest of this guide series.
7. Files migrating to archive may keep the timestamp filename or be renamed with a trailing slug: `2026-04-30T14-22-08-stripe-checkout.png`. The timestamp stays leading so chronological sort works.
8. Do not put non-screenshot images in this tree. If you save a downloaded image or a received image, it belongs in `~/Pictures/` not in `Screenshots/`.

## Worked example

The Desktop and Downloads are full of `Screenshot 2026-04-30 at 14.22.08.png` files.

1. Create `~/Pictures/Screenshots/inbox/`, `reference/`, and `archive/`.
2. Point the screenshot tool at the inbox: macOS `defaults write com.apple.screencapture location ~/Pictures/Screenshots/inbox && killall SystemUIServer`; on Linux use the tool's setting (Flameshot, Spectacle, GNOME Screenshot).
3. Set an ISO-timestamp filename pattern where the tool allows it: `2026-04-30T14-22-08.png`.
4. Triage weekly: keepers move to `reference/<purpose>/` with a descriptive name (`api-design-snippets/`), the rest is deleted.
5. Move long-term keepers to `archive/2026-04/` monthly.
6. Add a size guard: `du -sh ~/Pictures/Screenshots/inbox` in your weekly triage.

Captures stop scattering, and only the useful ones survive.

## Anti-patterns

- **Screenshots on the Desktop** — the macOS default. Pollutes your workspace, makes Desktop a graveyard, breaks the `files/desktop-zero-policy/` discipline. Reconfigure the default save location immediately.
- **No triage pass** — letting `inbox/` accumulate forever turns it into a write-only graveyard. Set a weekly calendar reminder; if you skip it, just delete the entire inbox.
- **Filing during capture** — pausing to drag each screenshot to a folder kills capture speed. Inbox-and-batch is faster.
- **Renaming inbox files speculatively** — "I'll rename this when I file it" — but you won't. The OS-generated timestamp is sufficient until triage.
- **Per-project screenshot folders inside the project** — sometimes appropriate for documentation but not for general reference; multiplying screenshot folders across projects defeats the central archive.
- **Cloud-only with no local copy** — losing access to a SaaS account vapourises your archive. Keep a local copy if the screenshots have long-term value.
- **Using `~/Pictures/Screenshots/` as the OS default and never subdividing** — without `inbox/`, the top level becomes the inbox and there's no clean place to put triaged keepers.
- **Hoarding** — refusing to delete because "I might need it" is the disease. The triage rule is "if I can't label it in 5 seconds, delete." This is healthy.
- **Manual screenshots into a date-only archive** — `2026-04-30/screenshot.png` skips the inbox-and-triage flow and you end up with thousands of unlabeled images per month directory.

## Scaling & failure modes

- **Sensitive content** (passwords, personal messages) ends up in screenshots; delete on triage and don't sync the inbox to the cloud.
- **Retina/4K captures** are large; convert reference images to compressed PNG or WebP if space matters.
- **Naming**: tools that can't use ISO patterns will need a rename step in the triage script.
- **Volume**: if the inbox regularly exceeds a few hundred files, triage more often rather than building more folders.

## Variants

- **auto-then-triage** (this guide) — inbox + weekly triage; recommended for most users.
- **auto-only with periodic delete-all** — set the OS to dump into `inbox/`, delete the entire inbox weekly via cron, never triage. Suitable for users who screenshot for ephemeral reasons only.
- **categorised-on-capture** — Flameshot or ShareX with hotkey-per-folder; press one shortcut to save into `reference/api-design-snippets/` directly. Eliminates triage but requires up-front decision-making at capture time.
- **screenshot-with-OCR** — pipe every screenshot through `tesseract` on capture and store the OCR text alongside; makes screenshots full-text searchable. Heavier setup, big payoff for engineers.
- **CleanShot or ShareX cloud-and-local** — uploads to a SaaS *and* keeps a local copy in the inbox flow.
- **inbox-only, no archive split** — `~/Pictures/Screenshots/` flat, with `reference/` for keepers; skip the `archive/YYYY-MM/` long-term split. Simpler, fine for low-volume users.
- **triage during the next idle window** — set a Hammerspoon, Keyboard Maestro, or AutoHotkey rule that prompts you to triage when the inbox passes 50 files. Reactive instead of scheduled.

## Adoption checklist

- [ ] The screenshot tool saves to the inbox by default.
- [ ] Filenames are ISO timestamps.
- [ ] Weekly triage leaves the inbox empty or nearly empty.
- [ ] Sensitive captures are deleted, not archived.
- [ ] The inbox isn't synced to shared cloud folders.

## Real-world projects using this

- **macOS `screencapture` defaults** — the canonical mechanism: `defaults write com.apple.screencapture location ~/Pictures/Screenshots/inbox; killall SystemUIServer` rebinds the default save path. https://support.apple.com/guide/mac-help/take-a-screenshot-mh26782/mac
- **Windows `Win+Shift+S`** — Snipping Tool's auto-save to `Pictures\Screenshots\` is configurable per the Snipping Tool settings panel; alternatively, redirect via the OneDrive backup setting.
- **Flameshot** — open-source screenshot tool with rich annotation; supports per-keybind save paths via its scripting API. https://flameshot.org/
- **Greenshot** — Windows screenshot tool with per-action save destinations and a "patterned filename" feature that produces ISO-timestamped names natively. https://getgreenshot.org/
- **ShareX** — heavyweight Windows tool with workflows that include "save to folder by category", "OCR after capture", "upload then file locally" — all configurable. https://getsharex.com/
- **CleanShot X** (macOS, commercial) — has both cloud and local flows; pairs well with this guide.
- **Hammerspoon** (macOS, free) — Lua scripting for OS automation; popular for triggering custom screenshot save flows. https://www.hammerspoon.org/
- **Hazel** (macOS, commercial) — rule-based file mover; the canonical Hazel use case is "watch `~/Pictures/Screenshots/inbox/` and delete files older than 30 days".

## Migration & references

To set up this layout from scratch:

```bash
# macOS — change the default screenshot save location:
mkdir -p ~/Pictures/Screenshots/{inbox,reference,archive}
defaults write com.apple.screencapture location ~/Pictures/Screenshots/inbox
killall SystemUIServer    # apply the change
defaults write com.apple.screencapture name "Screenshot"      # default prefix
defaults write com.apple.screencapture include-date -bool true  # default: ISO date
```

```bash
# Linux (GNOME) — gnome-screenshot saves to ~/Pictures/Screenshots by default;
# create the subdirectories and override the location via gsettings if needed:
mkdir -p ~/Pictures/Screenshots/{inbox,reference,archive}
# For Flameshot:
mkdir -p ~/Pictures/Screenshots/inbox
# Then in Flameshot's preferences, set "Save path" to ~/Pictures/Screenshots/inbox
```

For Windows:

```powershell
# Create the directory tree:
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Pictures\Screenshots\inbox","$env:USERPROFILE\Pictures\Screenshots\reference","$env:USERPROFILE\Pictures\Screenshots\archive"
# Then configure the Snipping Tool to auto-save to that inbox:
# Settings > Snipping Tool > Auto-save screenshots > Set folder
```

For weekly triage automation:

```bash
# Auto-delete inbox entries older than 14 days (cron-friendly):
find ~/Pictures/Screenshots/inbox -type f -mtime +14 -delete
```

To migrate from a flat `~/Pictures/Screenshots/`:

```bash
# Move all current screenshots into a one-time archive directory for retroactive triage:
mkdir -p ~/Pictures/Screenshots/archive/pre-migration
find ~/Pictures/Screenshots -maxdepth 1 -type f -name '*.png' -exec mv {} ~/Pictures/Screenshots/archive/pre-migration/ \;
```

Further reading:

- macOS `man screencapture` — full list of `defaults write` keys controlling capture behaviour.
- Flameshot user guide — https://flameshot.org/docs/
- ShareX workflow library — community-shared per-action configurations.
- `files/desktop-zero-policy/` — the related discipline of keeping the Desktop empty (which depends on screenshots not landing there).
- `files/photos-by-date-and-event/` — a layout for *photos*, distinct from screenshots.
- `principles/iso-date-formats/` — the timestamp convention used in inbox filenames.
- `principles/status-based-organization/` — the inbox/reference/archive split is an instance of status-based organisation applied to screenshots.

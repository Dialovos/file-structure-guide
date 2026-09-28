# Desktop zero-policy

## TL;DR

`~/Desktop/` is empty. That's the rule. If something lands there — a screenshot, a download, a drag-from-Finder — you have 24 hours to move it elsewhere or delete it. When you genuinely need a temporary scratch area for files in transit, use `~/desktop-staging/<YYYY-MM-DD>-from-desktop/` and time-box it. The Desktop is *not* a workspace, *not* a notes board, *not* a parking lot — it's a wallpaper. Every Desktop icon is a small visual interrupt and an open loop in your attention; zero icons means zero open loops at the OS level. The discipline is harder than it looks because the OS keeps trying to put things there (downloads, screenshots, "save to Desktop"), so half the work is reconfiguring defaults.

## Principles & why

The Desktop pulls in three directions, and a zero-policy resolves all three:

1. **The OS treats Desktop as the default scratch.** macOS dumps screenshots there until told otherwise. Windows does similar by historical convention. Browsers default downloads to Desktop or Downloads. Every "Save As" dialog suggests Desktop first. So *passively*, the Desktop fills up unless you actively redirect.

2. **Humans treat Desktop as the default focus area.** When you log in or wake the machine, the Desktop is what you see first. That makes it psychologically tempting to use as a to-do list — "I'll leave this PDF here so I remember to read it" — but a to-do list of files doesn't sort, doesn't search, and doesn't track completion. It's the worst possible to-do tool.

3. **The Desktop is multi-function by accident.** Without a policy, the Desktop is simultaneously the inbox, the workbench, the staging area, the active-document zone, and the long-term storage. None of those roles work well when colocated; this is `principles/one-purpose-per-directory/` violated at the worst possible location.

The zero-policy collapses all three: the Desktop is *one purpose only*, and that purpose is *visual calm*. Everything that wants to use it is redirected:

- Screenshots → `~/Pictures/Screenshots/inbox/` (see `files/screenshots-auto-flow/`).
- Downloads → `~/Downloads/` with a triage flow (see `files/downloads-triage/`).
- Active project files → the project directory (`~/code/`, `~/work/<project>/`, `~/notes/`).
- Genuinely-temporary in-transit files → `~/desktop-staging/<date>-from-desktop/` with a 30-day expiry.

The 24-hour SLA is not arbitrary. It's the longest interval over which you'll still remember why a file landed on the Desktop. Past that, you'll start treating it as background scenery, and within a week it'll be invisible to you — at which point it's fully indistinguishable from clutter.

## When to use

- Anyone who finds a clean visual environment calming and a cluttered one stressful.
- Knowledge workers who alt-tab to the Desktop frequently and need it to be a *neutral* surface, not a landing pad.
- Users with multi-monitor setups where the Desktop wallpaper is on display constantly.
- Anyone whose Desktop currently has more than 10 items — the symptom that this guide treats.
- Pair with `files/screenshots-auto-flow/` (which redirects screenshots away from Desktop) and `files/downloads-triage/` (which redirects downloads away from Desktop).
- macOS users who specifically want to avoid the "Stacks" auto-grouping feature, which is a compromise position rather than zero.

## When NOT to use

- Some workflows treat the Desktop as an active workspace — file managers like macOS use it as an extension of Finder, and many users genuinely work from Desktop icons. If that's working for you, this guide is not for you and that's fine.
- Users with macOS "Stacks" enabled who find the auto-grouped piles acceptable — Stacks is a softer, default-on compromise; if it's enough, you don't need this stricter rule.
- Heavily kiosk-style or single-purpose machines where the Desktop is configured by sysadmin policy and you don't control it.
- Linux DEs where there is no functional Desktop (e.g., tiling WMs like i3 or Sway with no DE) — the question doesn't apply.
- Users who actively use Desktop widgets, Rainmeter skins, or live-wallpaper systems where the surface is doing visible work — the constraint is different.

## Tree diagram

```
~/Desktop/                          ← always empty (or near-empty)
~/desktop-staging/
└── 2026-04-29-from-desktop/
```

## Naming rules

1. The Desktop's "structure" is its emptiness. `ls ~/Desktop` should produce no output (modulo `.DS_Store` on macOS, which is OS metadata you don't control).
2. The staging area lives at `~/desktop-staging/` — a sibling of `~/Desktop/`, not inside it. Inside-Desktop staging defeats the purpose because the staging directory itself becomes a Desktop icon.
3. Each staging session goes in its own dated subdirectory: `~/desktop-staging/YYYY-MM-DD-from-desktop/`. The leading date is for chronological sort; the `-from-desktop` suffix preserves provenance so you remember why this folder exists.
4. Files inside a staging session keep their original names — don't rename during staging. Renaming happens when the file moves to its real home.
5. A staging session has a 30-day expiry. If a file is still in `desktop-staging/` after 30 days, it gets deleted (not archived — deleted; the whole point of staging is that it's transient).
6. If a file in staging is genuinely needed long-term, it leaves staging and moves to its purpose-driven home (a project directory, `~/notes/`, `~/scans/`, etc.). Staging is *not* a long-term store.
7. macOS-specific: hide the `.DS_Store` files via shell config, and consider `defaults write com.apple.finder CreateDesktop -bool false; killall Finder` to disable Desktop icons entirely if you want strict zero.
8. Windows-specific: empty Desktop is achievable with the standard "Sort by > Auto arrange icons OFF + delete all icons" combo plus redirecting Downloads, Screenshots, and "Save to Desktop" defaults.

## Worked example

The desktop has 60 icons and finding the current one takes a minute.

1. Create `~/desktop-staging/` and move everything currently on the Desktop into `~/desktop-staging/2026-04-29-from-desktop/` in one go.
2. Sort that folder once: delete junk, file the rest in real homes (project folders, `~/Documents`, the archive).
3. Change defaults that write to the Desktop: the screenshot tool (see `screenshots-auto-flow`), browser downloads (see `downloads-triage`), and any app export folder.
4. Add a nightly check that lists anything on the Desktop older than a day, for example `find ~/Desktop -mindepth 1 -mtime +0` in a systemd timer or cron job that sends a notification.
5. Set a wallpaper you like. The Desktop's job is to be seen.

After a week the Desktop stays empty by habit and by defaults.

## Anti-patterns

- **"I'll just leave it here for now"** — the most common failure mode. *Now* is forever; without a 24-hour SLA, files accumulate.
- **Desktop as kanban** — using Desktop position to indicate task state ("urgent files top-left, archive bottom-right"). The OS doesn't preserve Desktop position reliably across reboots, monitor changes, or login switches; this is fragile and breaks silently.
- **Aliases / shortcuts to projects** — clutters the surface and provides no value over a Dock or Start Menu launcher.
- **Folder of folders ("Stuff", "Misc", "to-sort")** — meta-directories on the Desktop are just deferred decisions. Resolve them or delete them.
- **Screen-sharing surprise** — a cluttered Desktop you forget about until someone shares your screen reveals every embarrassing filename. A zero-Desktop policy solves this preemptively.
- **macOS Stacks as the answer** — Stacks tidies the visual presentation but doesn't solve the underlying problem (files still accumulate; you've just hidden them). Use Stacks as a transition, not a destination.
- **Inside-Desktop staging directory** — `~/Desktop/staging/` defeats the rule because the staging directory itself is now a Desktop icon. Staging must be a *sibling* of Desktop, not a child.
- **Permanent staging** — the `desktop-staging/` directory grows forever because nothing ever ages out. Implement the 30-day deletion or the staging area is just Desktop with extra steps.
- **Symlinks-to-projects on the Desktop** — same problem as aliases: clutter without value. Use the file manager's sidebar or your shell's `cd` aliases instead.

## Scaling & failure modes

- **Habit vs. defaults**: policies that rely on willpower fail; fix the apps that write there.
- **Shared machines and work profiles** may enforce their own Desktop redirects; apply the rule to the visible surface, not the mechanism.
- **Staging folders** become the new Desktop; the 24-hour timer and the dated name are the safeguard.
- **Cloud-synced Desktops** (OS-level folder backup) upload the mess; turn off desktop sync or keep the folder empty.

## Variants

- **strict-empty** (this guide) — `ls ~/Desktop` is literally empty; redirect every default that targets Desktop.
- **allow-N-items** — keep up to 5 icons on Desktop with a weekly sweep into staging or trash. Looser, easier to maintain, slightly less calm.
- **staging-only** — everything that lands on Desktop gets immediately moved to `~/Desktop/inbox/`; the visible Desktop has only that one inbox folder. A compromise that some find easier to maintain than strict-empty.
- **Stacks-managed** (macOS) — let Stacks group items by kind, date, or tag; live with the resulting compressed clutter. Default macOS behaviour with the feature on.
- **virtual-desktops-as-organisation** — using multiple virtual desktops (Spaces on macOS, Workspaces on GNOME, Virtual Desktops on Windows) so each is contextually clean even if one is messy. Not a substitute for the policy but a complement.
- **null-desktop** (`defaults write com.apple.finder CreateDesktop -bool false`) — disable the Desktop entirely on macOS so icons cannot be placed there. The most extreme variant; great for users who never use Desktop intentionally.
- **time-boxed exception** — allow Desktop icons during a specific work session (e.g., reviewing a stack of PDFs), but commit to clearing before logoff. Functions as deliberate tactical clutter.

## Adoption checklist

- [ ] `ls ~/Desktop` is empty.
- [ ] Screenshot, browser, and chat-app default save locations don't point at the Desktop.
- [ ] `~/desktop-staging/` entries are dated and emptied within a week.
- [ ] A reminder or timer flags files older than a day.
- [ ] Desktop cloud sync is disabled or irrelevant.

## Real-world projects using this

- **Cal Newport's "Deep Work" and "Digital Minimalism" writing** — Newport explicitly advocates for visual calm in your workspace; the empty Desktop is a recurring example. https://www.calnewport.com/
- **GTD (Getting Things Done) by David Allen** — the "inbox zero" philosophy generalises naturally to "desktop zero"; a clean visual workspace is part of the productivity stack. https://gettingthingsdone.com/
- **macOS "Stacks" auto-grouping** — Apple's own compromise solution, introduced in Mojave (2018); shows the OS has acknowledged the cluttered-Desktop problem. https://support.apple.com/guide/mac-help/use-stacks-mchl1531c84c/mac
- **The "Bullet Journal" community** — many practitioners extend the empty-Desktop idea to digital workspaces. https://bulletjournal.com/
- **r/unixporn and r/MacOSBeautiful** — communities of users who go to extremes for clean Desktops; many post strictly-zero Desktop screenshots as the norm.
- **Rectangle, Magnet, Amethyst, Rectangle Pro** — window managers that often pair with empty-Desktop philosophy by making the Desktop unnecessary as a window-target zone.
- **Apple's Stage Manager (macOS Ventura, 2022)** — Apple's continuing iteration on the same problem; Stage Manager treats the Desktop as a *real* workspace by hiding non-active windows, implicitly assuming Desktop is uncluttered.

## Migration & references

To take a cluttered Desktop and bring it to zero in one pass:

```bash
# macOS / Linux: stage everything currently on Desktop into a dated subdir of staging:
DATE=$(date +%Y-%m-%d)
mkdir -p ~/desktop-staging/${DATE}-from-desktop
mv ~/Desktop/* ~/desktop-staging/${DATE}-from-desktop/ 2>/dev/null
# Hidden files (rare but possible):
mv ~/Desktop/.[!.]* ~/desktop-staging/${DATE}-from-desktop/ 2>/dev/null

ls ~/Desktop      # should be empty (or just .DS_Store on macOS)
```

Then redirect defaults so nothing lands there going forward:

```bash
# macOS — stop screenshots from going to Desktop:
defaults write com.apple.screencapture location ~/Pictures/Screenshots/inbox
killall SystemUIServer

# macOS — disable Desktop icons entirely (the strict-empty extreme):
defaults write com.apple.finder CreateDesktop -bool false
killall Finder

# To re-enable later:
defaults write com.apple.finder CreateDesktop -bool true
killall Finder
```

For Windows:

```powershell
# Move current Desktop contents to a staging directory:
$date = Get-Date -Format "yyyy-MM-dd"
$staging = "$env:USERPROFILE\desktop-staging\$date-from-desktop"
New-Item -ItemType Directory -Force -Path $staging
Move-Item "$env:USERPROFILE\Desktop\*" $staging -Force

# Configure download defaults via browser settings; redirect "Save to Desktop"
# defaults via the application-by-application save preferences.
```

For the staging-area expiry cron:

```bash
# Delete staging-session subdirectories older than 30 days:
find ~/desktop-staging -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +
```

Further reading:

- macOS `defaults` write keys for Finder and screencapture — `man defaults`, `man screencapture`.
- "Inbox Zero" by Merlin Mann — the conceptual ancestor of "Desktop Zero".
- `files/downloads-triage/` — the related discipline for the Downloads directory.
- `files/screenshots-auto-flow/` — must be set up before this guide is sustainable; otherwise screenshots keep refilling the Desktop.
- `principles/one-purpose-per-directory/` — the underlying principle this guide enforces at the Desktop.
- `principles/status-based-organization/` — staging-with-expiry is a specific application of status-based organisation.

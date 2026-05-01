## TL;DR

A **digital garden** is a public-facing collection of notes published as a slowly-tended garden rather than a stream of finished blog posts. Drafts live alongside polished pieces, marked by *status* — `seedlings/` for rough captures, `budding/` for in-progress drafts, `evergreen/` for the published, refined work. The directory shape mirrors the publishing pipeline; visitors see the status alongside each note and can follow a piece from rough idea to mature essay over time. The defining philosophy is that **work-in-progress is part of the work** — readers see how thinking develops, you stop performing finished-ness, and the garden grows steadily without the binary "publish a finished post" gate. There's a `meta/` directory for the about page, colophon, RSS template, and similar plumbing, plus an `INDEX.md` that lists every note grouped by status. The metaphor was popularized by Maggie Appleton, Andy Matuschak, Tom Critchlow, and others in the early 2020s; it sits at the intersection of personal-wiki and personal-blog, deliberately rejecting both pure forms. It's an excellent fit for writers who want to publish process; a poor fit for private-only note-takers, who don't need the garden metaphor.

## Principles & why

Three principles define the garden shape.

1. **Publishing process, not just product.** A traditional blog publishes finished posts. A garden publishes *thinking in motion* — the seedling captured today might still be a seedling next year, or might mature into an evergreen essay six months from now. The status directories (`seedlings/`, `budding/`, `evergreen/`) make this maturation visible. The structural commitment: notes don't move silently from "draft" to "published"; they progress through visible stages with status surfaced to readers.
2. **Ownership of work-in-progress.** Twitter / Substack / Medium reward polish and discourage half-formed thoughts. A garden inverts that: half-formed thoughts are first-class citizens because *that's where the value lives* for both writer and reader. The reader sees how thinking actually develops; the writer is freed from the "finished" performance. The directory structure encodes this — there is no "drafts" folder hidden from readers; `seedlings/` is shipped.
3. **Bidirectional links and emergent structure.** Most gardens are heavily linked — notes reference notes via `[[wikilinks]]`, and the rendered site exposes backlinks. This is partly a Roam/Logseq inheritance and partly a recognition that a *garden* is browsed by following links, not by reading in chronological order (the way a blog is). The `INDEX.md` gives a high-level entry point grouped by status; from there, readers wander.

The structural consequence: a garden is published as a static site (Jekyll, Hugo, Eleventy, Quartz, Obsidian Publish, custom React) where the source layout maps onto the published layout. A note in `seedlings/` renders with a "Seedling" badge; a note in `evergreen/` renders with an "Evergreen" badge; backlinks render at the foot of each page; the `INDEX.md` becomes the home page.

The metaphor breaks down if pushed too hard — real gardens don't have categorical stages; gardens are messier than three folders. Still, the seedling/budding/evergreen split is the most-adopted convention because it's simple enough to maintain.

## When to use

- **You publish.** A blog, personal wiki, public notes site. The garden metaphor is fundamentally about *publishing* — sharing process is the whole point.
- **You write at varying levels of polish.** You produce both quick captures and longer-form essays, and you want to publish both. A pure blog forces everything into the "finished essay" mold; a garden does not.
- **You want bidirectional links and backlinks public-facing.** The garden's Linked-References feel — built by tools like Quartz, Obsidian Publish, or hand-rolled — is core to the experience.
- **You buy the philosophy.** The garden is a stance: it says "I don't know yet" is a valid public position. If that resonates, the metaphor works. If it feels self-indulgent, it won't.
- **You write slowly and want consistent visible progress.** Gardens reward steady tending more than blogs reward steady publishing.

## When NOT to use

- **Private notes only.** The garden metaphor is about *publishing* progress. If your notes never leave your machine, you don't need a garden — use a regular note system (Obsidian vault, PARA, Zettelkasten, etc.).
- **Pure essay/blog publishing.** If you only publish polished essays, the seedling/budding stages are dead weight. A blog (Hugo, Astro, Substack) is simpler.
- **You hate showing unfinished work.** Some writers find shipping seedlings deeply uncomfortable; if you're one of them, fighting the discomfort to maintain a garden is grim. Keep your unfinished work private; publish only what's ready.
- **Heavy collaboration.** Gardens are fundamentally personal — they're someone's mind, made walkable. Multi-author gardens exist but they confuse the "you can see the writer thinking" affordance.
- **Newsletter or feed-driven audiences.** Subscribers who expect a steady stream of posts won't engage with a garden the same way. RSS helps, but a garden's reading model is wandering, not subscribing. Pick the model that matches what you want.

## Tree diagram

```
garden/
├── seedlings/                  ← rough captures
├── budding/                    ← in-progress drafts
├── evergreen/                  ← published, refined
├── meta/                       ← about, colophon, RSS template
└── INDEX.md                    ← garden home page
```

The three status directories reflect the publishing pipeline. `meta/` holds the about page, colophon, and similar plumbing. `INDEX.md` is the home page — typically lists notes grouped by status with most-recent or most-loved at the top.

## Naming rules

- **Note files**: kebab-case, descriptive — `attention-residue.md`, `notes-on-cargo.md`, `essay-on-craft.md`. Avoid date prefixes; gardens are topic-organized, not date-organized.
- **Status directories**: `seedlings/`, `budding/`, `evergreen/`. The `seedling → budding → evergreen` triplet is the most-adopted naming. Some gardens use `notes/` `posts/` `essays/` instead — defensible, but loses the gardening metaphor's cohesion.
- **`meta/` files**: `about.md`, `colophon.md`, `now.md`, `rss.xml`, `feed.json`. Convention names; renders cleanly in most static-site setups.
- **`INDEX.md`**: at the garden root. The home page. Most static-site generators look for `index.md` or `INDEX.md`; check yours and use what it expects.
- **Status badges**: many gardens render a status badge at the top of each note based on which directory it lives in. Don't encode status in the filename; encode it in the directory.
- **Internal links**: `[[wikilinks]]` are the convention because most garden builders (Quartz, Obsidian Publish, Eleventy with plugins) expand them and build backlinks. Use them; don't try to fight the wiki-link affordance.

## Anti-patterns

- **Hiding `seedlings/` from the published site.** Defeats the whole metaphor. The seedling-on-display *is* the garden's point. Publish them; let them be rough.
- **Endless seedlings, no growth.** A garden that only ever has seedlings is a graveyard. Periodically (monthly, quarterly) revisit seedlings; promote ripe ones to budding, prune dead ones, refine some toward evergreen. The tending is the practice.
- **Treating evergreens as immutable.** "Evergreen" doesn't mean *finished*. Evergreens get pruned, expanded, edited as your thinking evolves. The status reflects current polish, not chronological birth date.
- **Date-based filenames.** Gardens are topic-organized; date-based filenames push you toward chronological reading, which is what blogs do. Use topic-named files; let the metadata track when each was first written and last tended.
- **Polished-sounding seedlings.** A seedling should *look* like a seedling — a few sentences, a question, a fragment. Writing seedlings in finished prose blurs the categories and undermines the trust readers place in the labels.
- **MOC overgrowth.** Some gardens evolve a thick layer of MOCs (Maps of Content) until the garden is mostly index pages. The notes-to-index ratio should stay heavily on the notes side. Use MOCs sparingly.

## Variants

- **Seedling-budding-evergreen** (this guide). Maggie-Appleton-style; the most-adopted shape.
- **Draft-published binary.** Two folders: `drafts/` and `published/`. Simpler; loses the maturation gradient. Defensible if the gradient feels precious.
- **Mike Caulfield's "stocks and flows"** — a theoretical framing that distinguishes accumulating notes (stocks) from time-bound posts (flows). Maps onto evergreen vs seedling abstractly. More vocabulary than directory shape, but informs many gardens' structure.
- **Andy Matuschak's "evergreen notes"** — heavier on evergreens, lighter on seedlings; the public site is mostly mature notes with very few in-progress ones. Different philosophy from Maggie-style; both are gardens.
- **Newsletter-plus-garden hybrid.** A newsletter for finished essays, a garden for everything else. Both publish; neither is forced into the other's shape.

## Real-world projects using this

- **Maggie Appleton's garden** (maggieappleton.com/garden) — the canonical reference; defined the seedling-budding-evergreen vocabulary and the visual conventions many other gardens copy.
- **Andy Matuschak's published notes** (notes.andymatuschak.org) — the evergreen-notes-heavy variant; demonstrates a more research-y / philosophical tone.
- **Tom Critchlow's garden** (tomcritchlow.com/wiki) — early adopter of the garden metaphor; influential writeup "Of Digital Streams, Campfires, and Gardens" worth reading.
- **Joel Hooks' garden** (joelhooks.com) — combines a blog and garden in one site; pragmatic implementation.
- **Jacky Alciné's writing on gardens** (jacky.wtf) — thoughtful pieces on the social and political dimensions of public-facing notes; a perspective complementary to the more product-oriented writeups.

## Migration & references

- **From a personal blog**: keep the polished posts as `evergreen/`. Drop in any private-but-ready-enough notes as `budding/`. Start adding seedlings as the practice; the evergreen layer grows over time.
- **From an Obsidian vault**: identify the notes you'd be willing to publish. Move them under `seedlings/`/`budding/`/`evergreen/` based on current polish. **Obsidian Publish** is the simplest path — it publishes from your vault with backlinks and graph view. **Quartz** (jzhao.xyz/quartz) is a popular open-source alternative.
- **From Roam Research / Logseq**: export the graph as markdown, drop into `seedlings/` initially, manually promote as you tend. The wikilink syntax is portable.
- **Tooling**: **Quartz**, **Eleventy + plugins**, **Hugo + theme**, **Astro**, **Next.js + custom**, **Obsidian Publish**, **Notion-as-CMS** all power gardens. Quartz is the closest to "drop a markdown folder in, get a garden out".
- **References**:
  - `maggieappleton.com/garden` — the canonical garden.
  - `notes.andymatuschak.org` — the evergreen variant.
  - `tomcritchlow.com/wiki` — Tom Critchlow's writeups on the metaphor.
  - `quartz.jzhao.xyz` — Quartz, the popular open-source garden builder.
  - Sibling guides: `notes/evergreen-notes/` (the philosophy that powers the evergreen layer), `notes/atomic-notes/` (the underlying note discipline), `notes/maps-of-content/` (MOCs as garden navigation), `notes/lyt-linking-your-thinking/` (Nick Milo's framework, a frequent garden underpinning).

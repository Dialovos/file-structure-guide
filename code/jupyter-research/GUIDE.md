## TL;DR

The **Jupyter research** layout is the structure for projects whose primary artifact is *the notebook itself* — academic research, exploratory analyses, papers reproducible from a notebook, blog-post-style data essays. It's deliberately lighter than `cookiecutter-data-science`: there's no `Makefile`-driven pipeline, no rigid `data/{raw,interim,processed,external}/` four-tier hierarchy, no opinion that code must "graduate" into an installable package. Instead: `notebooks/` is the canonical artifact (numbered by execution order, `01-data-loading.ipynb`, `02-eda.ipynb`, ...); `data/raw/` and `data/processed/` give the minimum data lifecycle; `figures/` is where polished plots get saved; an *optional* `paper/` directory holds the LaTeX or Quarto write-up; and an *optional* `src/` directory holds utility code that grew too gnarly to live inline in notebooks. The mental model: notebooks are first-class research output, not a transient stage. They get named, numbered, kept clean, executed top-to-bottom for reproducibility, and (often) shipped alongside the paper as supplementary material. Used well, this layout produces repos where a reader can open `notebooks/04-modeling.ipynb` and see the entire reasoning chain — not just the result. Used poorly, it produces 47 untitled notebooks named `Untitled.ipynb` through `Untitled46.ipynb`. The naming convention is half of the value of the structure.

## Principles & why

The Jupyter research layout is shaped by five principles, each enforced by convention rather than tooling.

1. **Notebooks are the output, not the scratchpad.** Treat them like a paper section: ordered, narrated, top-to-bottom executable. The README points to `notebooks/01-data-loading.ipynb` first; readers consume the project by reading notebooks in order.
2. **Notebook order is encoded in filenames.** `01-data-loading.ipynb`, `02-eda.ipynb`, `03-feature-engineering.ipynb`, `04-modeling.ipynb`. Two-digit prefix (`01-`, not `1-`) so file managers sort them lexically and you have room for `02a-*`, `02b-*` siblings if a step splits.
3. **Data has a minimum two-tier lifecycle.** `data/raw/` for the original download (immutable, gitignored); `data/processed/` for derived outputs. You can grow this into the four-tier CCDS scheme if the project gets bigger, but two tiers is enough for most research.
4. **Figures live in `figures/`, dated for traceability.** A plot for a paper figure is saved to `figures/2026-04-30-eda-distributions.png`. The date prefix means that when you regenerate the figure two months later, you don't accidentally overwrite the version that's already in the LaTeX `\includegraphics`. This is the single most-overlooked convention; it saves drafts.
5. **`src/` is optional and exists only if needed.** If a notebook re-uses a 30-line plotting helper, factor it into `src/utils.py` and import. If your project has *no* such code, omit `src/` entirely. Don't create empty scaffolding "for later." The same applies to `paper/` — only there if you're writing a paper.

A sixth, softer principle: **`environment.yml` (conda) or `pyproject.toml` (pip/uv) is in the repo root, not buried.** Reproducibility starts with "what packages did this run with?" and ends with "what versions?" Either tool works; conda is more common in scientific computing because it handles non-Python deps (CUDA, BLAS, etc.); pip is fine for pure-Python work. Pin versions for true reproducibility.

## When to use

- **Academic research** — papers, dissertations, NeurIPS / ICML / Nature reproducibility-track repos.
- **Exploratory analyses** that may or may not become production code; the question is "what does the data say?" not "how do I deploy this?"
- **Pedagogical projects** — fast.ai courses, university teaching repos, reproducible textbook examples.
- **Blog post / essay backing** — data-driven blog posts where the notebook *is* the article (rendered via nbconvert, Quarto, or Jupyter Book).
- **Single-author or small-team research** where the formality of CCDS pipelines / Makefiles is overhead.
- **Prototyping a paper before committing to a production codebase.** When the project graduates, migrate to `cookiecutter-data-science/` or a domain-specific layout.

## When NOT to use

- **Production ML pipelines.** Use `cookiecutter-data-science/`. The `Makefile`-driven, src-promoted, multi-stage data pipeline is a better fit.
- **Anything where `src/` is the canonical artifact.** Notebooks become the throwaway demo layer in that case — use `python-src-layout/`.
- **Multi-developer projects with strong CI requirements.** Notebooks diff badly; merge conflicts in `.ipynb` files are painful. Mitigate with `nbstripout` + `jupytext`, or move to a non-notebook layout.
- **Projects that ship a library to other developers.** Library users want a real package (`pip install mylib`), not a notebook to clone.
- **Real-time / streaming.** Notebooks assume a batch, top-to-bottom execution model.

## Tree diagram

```
research-project/
├── README.md
├── pyproject.toml          ← or environment.yml for conda
├── notebooks/
│   ├── 01-data-loading.ipynb
│   ├── 02-eda.ipynb
│   ├── 03-feature-engineering.ipynb
│   └── 04-modeling.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── figures/
│   └── 2026-04-30-eda-distributions.png
├── paper/                  ← optional: LaTeX/Quarto write-up
│   ├── main.tex
│   └── references.bib
└── src/                    ← optional: utility code refactored out of notebooks
    └── utils.py
```

## Naming rules

- **Repo name**: kebab-case (`predict-customer-churn-research/`, `arxiv-figures-replication/`).
- **Notebook files**: `<NN>-<short-description>.ipynb` with two-digit zero-padded prefix and kebab-case description. `01-data-loading.ipynb`, `02-eda.ipynb`, `03a-feature-engineering-numerical.ipynb`. The prefix is for execution order, not a step number; `02a-`, `02b-` lets you insert sibling notebooks without renumbering everything.
- **Data files**: descriptive snake_case + extension. `customers_2024.csv`, `embeddings.parquet`. Avoid `data.csv` or `final.csv` — be specific.
- **Figures**: `YYYY-MM-DD-<purpose>.png` (or `.pdf` for LaTeX). `2026-04-30-eda-distributions.png`, `2026-04-30-roc-curve.pdf`. Date-prefixed so iterations don't overwrite past versions.
- **`src/` files**: lowercase snake_case Python convention. `utils.py`, `data_loading.py`, `plotting.py`.
- **Paper files**: standard LaTeX conventions. `main.tex`, `references.bib`, `appendix.tex`. Quarto: `index.qmd`, `references.qmd`.

## Anti-patterns

- **`Untitled.ipynb`, `Untitled1.ipynb`, ..., `Untitled27.ipynb`.** The default Jupyter filename. Always rename. The first notebook a stranger opens should be `01-*.ipynb`, not random.
- **Notebooks that don't run top-to-bottom.** A notebook that requires "skip cell 7, run cell 12 first" is broken. Restart the kernel and Run All as a final step before committing.
- **Out-of-order cell execution numbers.** A reader sees cells `In[1]`, `In[5]`, `In[2]`, `In[12]`. Restart kernel + Run All before committing; or use `nbstripout` to strip outputs entirely.
- **Hardcoded absolute paths.** `pd.read_csv('/Users/jane/research/data/foo.csv')` works for Jane's laptop and breaks for everyone else. Use `Path(__file__).parent.parent / "data" / "raw" / "foo.csv"` or a notebook-relative `Path("../data/raw/foo.csv")`.
- **Committing data to git.** `data/raw/` is gitignored except for `.gitkeep`. Real data lives elsewhere — `wget` script in the README, S3, Zenodo, OSF, or a `data_loading.py` that downloads it.
- **One giant notebook.** A single 80-cell notebook covering data, features, models, and figures is unreviewable. Split into the numbered four-or-five-notebook series.
- **Committing `.ipynb_checkpoints/`.** Always gitignored. (The Jupyter team's recommendation; the directory is a local-cache, not a versioned artifact.)
- **Committing notebook outputs by default in noisy projects.** Outputs in cells inflate the diff and leak data. Use `nbstripout` (a pre-commit hook) to strip outputs on commit, then `nbconvert` for HTML exports if the rendered version matters. Some projects keep outputs (the rendered figure *is* the result); the choice is project-specific but should be deliberate.
- **Mixing paper-LaTeX build artifacts into git.** `*.aux`, `*.bbl`, `*.log`, `*.pdf` — gitignore them all. Commit `main.tex` and `references.bib`; let CI or the reader build the PDF.
- **Deleting `src/utils.py` and pasting the helper back into the notebook.** The point of `src/` is to share. Resist the urge.

## Variants

- **Notebooks-only** — no `src/`, no `paper/`. Just `notebooks/`, `data/`, `figures/`. Smallest viable structure; common for blog-post backing.
- **Notebooks + utility-src (this guide)** — adds `src/utils.py` (and friends) for code factored out of notebooks. The most common research-project shape.
- **Notebooks + paper** — adds `paper/main.tex` for the LaTeX write-up. Common for academic submissions.
- **Quarto-rendered** — replaces `notebooks/` with `*.qmd` files (Quarto markdown with executable code blocks). Renders to HTML, PDF, or LaTeX from one source. Increasingly popular in 2025-2026.
- **Jupyter Book** — `notebooks/` + a `_config.yml` and `_toc.yml`; renders to a multi-page Jupyter Book site. Perfect for textbook-style projects.
- **NB + jupytext-paired** — every `.ipynb` has a paired `.py` (jupytext sync). The `.py` versions are diff-friendly, the `.ipynb` versions execute. Best of both worlds for git workflows.
- **Reproducibility-strict** — adds `Dockerfile` + `binder/` so a reader can launch the whole project in MyBinder.org with one click. Common for NeurIPS / ICLR reproducibility-track submissions.

## Real-world projects using this

- **Berkeley reproducible-research class examples** — Berkeley's *Stat 159* and similar courses publish student / staff repos in this exact layout (notebooks numbered, `data/`, `figures/`, sometimes `paper/`).
- **Quarto example projects** — the Quarto docs ship with sample research-style projects; layout is essentially this guide with `*.qmd` instead of `*.ipynb`.
- **Jeremy Howard's fast.ai course notebooks** (`fastai/fastbook`, `fastai/course22`) — numbered notebooks (`01_intro.ipynb`, `02_production.ipynb`, ...), data downloaded on first run, polished as a published book.
- **NeurIPS / ICLR reproducibility-track repos** — many follow this layout. Searches like "github.com NeurIPS 2024 paper code" surface examples.
- **Jupyter Book gallery** — `executablebooks.org/en/latest/gallery.html` lists production research projects using the layout.
- **Many published Kaggle solutions** — top Kaggle competition solutions are often posted as Jupyter-research repos with numbered notebooks for the competition stages.
- **OSF and Zenodo "code accompanying paper" deposits** — published reproducibility archives lean heavily on this shape.

## Migration & references

- **From a single sprawling notebook to the structured layout**: split the notebook into thematic sections (data loading, EDA, features, modeling, figures). Save each as `0N-*.ipynb`. Move helpers into `src/utils.py`. Update README to point at the notebooks in order.
- **From this layout to CCDS** when the project graduates to production: rename `notebooks/` to `notebooks/` (already correct), expand `data/{raw,processed}` to `data/{raw,interim,processed,external}`, promote `src/utils.py` into `src/<package>/` with `pyproject.toml` packaging, add a `Makefile`. The notebooks survive intact.
- **Adding Quarto rendering**: install Quarto, add `_quarto.yml` at the root, run `quarto render`. Notebooks become Quarto sources without renaming if you keep `.ipynb`; otherwise convert to `.qmd`.
- **Adding Jupyter Book**: `pip install jupyter-book`, add `_config.yml` and `_toc.yml` listing the notebooks, run `jupyter-book build .`. The book builds into `_build/`.
- **Adding a paper**: create `paper/main.tex`, `paper/references.bib`. Reference figures from `../figures/2026-04-30-*.pdf` (relative path). Build the PDF with `latexmk -pdf paper/main.tex`.
- **Adding `nbstripout`**: `pip install nbstripout`, then `nbstripout --install` (per-repo). Notebook outputs strip on every `git add`.
- **References**:
  - Jupyter docs (jupyter.org) — official notebook conventions.
  - The *Reproducible Research* literature — Stodden et al., Wilson et al., Munafò et al. (good-enough-practices papers).
  - Quarto docs (quarto.org) — Quarto research project tutorials.
  - Jupyter Book docs (jupyterbook.org).
  - Sibling guides: `code/cookiecutter-data-science/` (heavier production sibling), `code/python-src-layout/` (the underlying Python convention if you grow `src/`).

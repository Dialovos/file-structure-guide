## TL;DR

A **research lab notebook** records *what you tried, why, and what happened*, in an order and with enough detail that you (or a colleague) can reproduce or challenge it later. Keep two layers. A **chronological notebook** (`notebook/YYYY-MM-DD.md`) is the running log: intentions, observations, dead ends. **Experiments** (`experiments/NNNN-slug/`) are numbered, self-contained records, each starting with a **question and hypothesis written before the run**, followed by the protocol, links to raw data, the analysis, the result, and a conclusion, including when the answer is "no." A top-level `questions.md` lists open questions, and `decisions/` records choices that changed the direction of the work. Raw data is immutable and referenced, not copied. The result is research that survives your own memory: every claim traces to an experiment, every experiment to a question, every question to a day when you thought it mattered.

## Principles & why

1. **Write the hypothesis before the run.** A prediction made in advance is a test; a story told afterward is a rationalization. Recording it first also reveals when the experiment cannot actually fail.
2. **Negative results are results.** A failed experiment saves someone (often you) from repeating it. Record what was tried and why it didn't work, with the same care as successes.
3. **Chronology and topic are different views.** The dated notebook captures process and context; numbered experiments capture self-contained conclusions. Keep both, and link between them.
4. **Raw data is immutable.** Analysis reads raw data and writes derived data elsewhere; never edit the original (see `stable-vs-volatile-separation`).
5. **Reproducibility is a design goal.** Record versions, parameters, seeds, environment, and the exact commands, so a stranger can rerun the analysis.
6. **Decisions leave a trail.** When the direction changes, write down why, at the time (see `decision-records-adr`).

## When to use

- **Graduate research, thesis work, and lab science** with experiments over weeks or months.
- **Applied ML and data research** where many runs and hypotheses accumulate (pair with `ml-experiment-project`).
- **Engineering investigations**: performance work, migrations, debugging campaigns.
- **Independent researchers** who need to reconstruct their own reasoning months later.

## When NOT to use

- **Literature management.** Papers and summaries belong in `literature-review-structure`.
- **Code organization.** Analysis code goes in a project repository (see `jupyter-research`, `cookiecutter-data-science`); the notebook links to it by commit.
- **Ephemeral exploration** where no result will be kept; a scratch file is enough.
- **Shared official lab records** that require signed, tamper-evident, or regulated formats; follow your institution's electronic lab notebook system and use this layout for personal working notes only.

## Tree diagram

```
lab/
├── README.md                          ← project overview, current focus
├── questions.md                       ← open questions, newest first
├── notebook/
│   ├── 2026-04-29.md                  ← running daily log
│   └── 2026-04-30.md
├── experiments/
│   ├── 0001-baseline-reproduction/
│   │   ├── README.md                  ← question, hypothesis, result, conclusion
│   │   ├── protocol.md                ← exact steps, parameters, environment
│   │   ├── raw/                       ← pointers or immutable data
│   │   ├── analysis/                  ← scripts and derived data
│   │   └── results.md
│   └── 0002-wider-embedding/
├── decisions/
│   └── 0001-drop-dataset-b.md
└── literature/                        ← see literature-review-structure
```

## Naming rules

- **Notebook entries** are `YYYY-MM-DD.md`, one per working day; several entries in a day are sections in one file (see `iso-date-formats`).
- **Experiments** are `NNNN-slug/`, with a four-digit sequence number assigned when the experiment is *planned* and a slug that says what changes (`0007-wider-embedding`).
- **Standard files** inside an experiment keep the same names every time: `README.md`, `protocol.md`, `results.md`, and `raw/`, `analysis/`.
- **Decisions** are `NNNN-slug.md` in `decisions/`, as ADRs.
- **Questions** carry stable IDs in `questions.md` (`Q12`) so notebook entries and experiments can cite them.
- **Data files** include the date or run ID and never a "final" suffix (see `versioning-in-paths`).

## Worked example

You suspect that a wider embedding layer improves validation accuracy, and you want a record that will hold up when someone (including you) asks in six months.

1. In `questions.md`, add: `Q12: Does widening the embedding from 64 to 128 improve validation accuracy on dataset A?` with the date.
2. Create `experiments/0007-wider-embedding/README.md` before running anything:
   - Question: Q12.
   - Hypothesis: accuracy improves by at least 1 percentage point; if it improves by less, the width is not the bottleneck.
   - Design: same seeds (0 to 4), same data split, only width changes; metric: validation accuracy at the best epoch.
3. Write `protocol.md`: commit hash of the code, data version (pointer or hash), exact command, environment (library versions, hardware), and seeds.
4. Run it. During the day, log in `notebook/2026-04-30.md`: what you started, what surprised you (a run crashed; the loader was slow), and any deviation from the protocol.
5. Put raw outputs in `raw/` (or a pointer to where they live), and analysis scripts in `analysis/`; derived tables go in `analysis/`, never over the raw files.
6. Write `results.md` with the numbers and a plot, including run-to-run spread across seeds.
7. Finish the README with a conclusion: "Accuracy improved by 0.3 points, within seed noise; hypothesis not supported. Width is unlikely to be the bottleneck." Update `questions.md` (Q12 answered; new Q13 about learning rate).
8. If the result changes the plan, write `decisions/0002-stop-widening-embedding.md` with the reasoning.

Six months later, the conclusion, its evidence, and how to rerun it are all in one folder.

## Anti-patterns

- **Writing the hypothesis after seeing the result.** It turns the notebook into a justification.
- **Recording only successes.** You will repeat the failures, and readers will overestimate how often things work.
- **Editing old entries** to look tidier. Add dated corrections; the original record is the evidence.
- **Overwriting raw data** with cleaned versions. Keep raw immutable and derive.
- **Results without conditions**: a number with no seed, version, or parameters can't be reproduced.
- **Screenshots of plots as the only record.** Save the data and the script that produced the plot.
- **One giant notes file** for a year of work. Split by day and by experiment, and index.

## Scaling & failure modes

- **Many experiments**: keep an `experiments/INDEX.md` table (number, question, status, one-line conclusion), and generate it with a script if needed (see `indexes-and-mocs`).
- **Collaboration**: agree on ID assignment (one person allocates numbers, or use per-person prefixes) to avoid collisions.
- **Large data**: store data outside git with pointers and hashes (see `large-files-and-binary-assets`), and record locations in `protocol.md`.
- **Long projects**: write a monthly summary in `notebook/` pointing to the important experiments and decisions; it's the fastest way to re-enter the work.
- **Publication**: when writing a paper, each claim should cite an experiment ID; a script can check that cited IDs exist and have conclusions.
- **Regulated settings**: use an institution-approved electronic lab notebook for official records, and treat this repository as working notes.

## Variants

- **Markdown files in git** (this guide): plain text, diffable, portable.
- **Jupyter-based notebook**: each experiment is a notebook; keep the README-first discipline in the first cell (see `jupyter-research`).
- **Electronic lab notebook (ELN) software**: hosted products with audit trails; use this layout for the local working copy.
- **Tracker-first ML**: an experiment tracker holds runs, and the notebook holds hypotheses, conclusions, and decisions with links to run IDs.
- **Pre-registration style**: for confirmatory studies, freeze the README (hypothesis, design, analysis plan) in a commit or public registry before collecting data.

## Adoption checklist

- [ ] Each experiment README has a question and a hypothesis committed before the run.
- [ ] Each experiment records code version, data version, environment, seeds, and exact commands.
- [ ] Raw data is never modified; derived data lives in `analysis/`.
- [ ] Negative and inconclusive results have conclusions recorded.
- [ ] `questions.md` and an experiments index are current.
- [ ] Decisions that changed direction are recorded in `decisions/`.

## Real-world projects using this

- **Lab notebooks in science** are a long-established practice; research-integrity guidance from universities and funding agencies commonly asks for contemporaneous, dated, complete records.
- **Pre-registration** (the Center for Open Science's OSF Registries and AsPredicted) formalizes writing hypotheses and analysis plans before data collection.
- **"Good enough practices in scientific computing"** (Wilson et al., 2017) recommends project layouts and record-keeping close to those used here.
- **Cookiecutter Data Science** and **DVC** document the data and pipeline side of reproducible research.
- **Open notebook science** projects (for example, Jean-Claude Bradley's Open Notebook Science) published lab notebooks in full.

## Migration & references

- **From scattered notes:** start with new experiments in the structure; backfill only experiments still relevant, marking the reconstructed ones as retrospective.
- **From a single notebook file:** split by date into `notebook/`, and pull out each distinct experiment into `experiments/NNNN-slug/`.
- **From an ELN:** export entries as PDF or Markdown into `notebook/` with dates, and keep the ELN as the official record.
- **References:**
  - `code/jupyter-research/` and `code/ml-experiment-project/` for code and runs.
  - `notes/literature-review-structure/` for papers and summaries.
  - `principles/decision-records-adr/` for `decisions/`.
  - `principles/stable-vs-volatile-separation/` for raw versus derived data.

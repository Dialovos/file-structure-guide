## TL;DR

Git is built for text. Large or frequently changing **binary files** (datasets, model checkpoints, videos, design files, compiled artifacts) bloat every clone, because git stores every version forever. Decide early where each kind of large file lives. **Small, stable binaries** (icons, a logo, a test fixture under a few megabytes) can stay in git. **Large or changing assets** go in a pointer-based system (Git LFS, DVC) or an external store (object storage, an artifact registry), with only a small pointer or manifest committed. **Generated binaries** are never committed at all (see `generated-vs-source-separation`). Put large assets in a clearly named directory, document how to fetch them, and record checksums so a fetch can be verified. The goal: a fresh clone is fast, the history stays small, and anyone can reproduce the full working set with one documented command.

## Principles & why

1. **History is forever.** A 200 MB file committed once and deleted later still lives in every clone. Size decisions have to be made before the commit, because removal requires rewriting history.
2. **Pointers beat payloads.** A tiny text pointer (LFS pointer file, `.dvc` file, manifest with checksums) versions the identity of a large file in git, while the bytes live elsewhere.
3. **Integrity comes from checksums.** A manifest with hashes lets a fetch step verify that it got the right bytes, and lets reviews see when an asset changed.
4. **Separate by change rate and reproducibility.** Immutable inputs, regenerable outputs, and hand-edited assets each need a different home (see `stable-vs-volatile-separation`).
5. **Cloning must stay cheap.** Contributors who only need code shouldn't download gigabytes of media; fetch on demand.
6. **Licenses and privacy apply to files too.** A dataset or image may not be redistributable; know what is public before pushing.

## When to use

- **Machine-learning projects** with datasets, checkpoints, and embeddings.
- **Game and design projects** with textures, audio, and source art files.
- **Websites and documentation** with large images or video.
- **Repositories with test fixtures** above a few megabytes.
- **Any repo where `git count-objects -vH` or clone time has started to hurt.**

## When NOT to use

- **Don't add LFS or DVC for a handful of small images.** The tooling has a cost (setup, credentials, quotas); a few hundred kilobytes in git is fine.
- **Don't store secrets or credentials as "binary files"** in any of these systems (see `config-and-secrets-placement`).
- **Don't use git for backups of media libraries or databases.** That is a job for backup tools (see `backup-3-2-1-layout`).
- **Don't version generated artifacts** that can be rebuilt; build them in CI and publish to a registry.

## Tree diagram

```
project/
├── src/
├── assets/
│   ├── icons/               ← small, stable: committed directly
│   └── media/               ← large: tracked by pointers
│       ├── intro.mp4        ← git-lfs pointer in the repo, bytes in LFS
│       └── media.manifest   ← names, sizes, sha256
├── data/
│   ├── raw.dvc              ← DVC pointer to the dataset in remote storage
│   └── .gitignore           ← DVC adds the real data path here
├── .gitattributes           ← `assets/media/** filter=lfs diff=lfs merge=lfs -text`
└── README.md                ← "How to fetch the large files" section
```

## Naming rules

- **Large-asset directories** are named for their role and separated from code: `assets/media/`, `data/raw/`, `models/`.
- **Pointer and manifest files** keep the asset's name plus a suffix (`raw.dvc`, `media.manifest`), so the pointer sits next to what it describes.
- **Versioned assets** are versioned by git or storage version, not by filename suffix (see `versioning-in-paths`); for immutable published artifacts, put the version in the release name.
- **Attributes** live in `.gitattributes` at the repository root, with one pattern per asset directory.
- **Checksums** use `sha256` and are recorded as `<hash>  <path>` in a text manifest.

## Worked example

A repository has grown to 2.4 GB and clones take ten minutes. Most of the weight is old `.psd` and `.mp4` files.

1. Find the weight: `git count-objects -vH` and `git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sort -k3 -n -r | head -20`.
2. Decide per file: keep small stable icons in git; move large media to LFS (`git lfs track "assets/media/**"`), and datasets to DVC (`dvc add data/raw`).
3. Migrate history so old blobs also become pointers: `git lfs migrate import --include="assets/media/**" --everything` on a fresh mirror clone. Coordinate with the team, because this rewrites history.
4. Add a `README` section on fetching (`git lfs pull`, `dvc pull`) and a CI step that runs it.
5. Record the checksums in a manifest and add a CI check that verifies them.
6. Ask contributors to re-clone.

Clone size drops to the size of the code plus pointers, and large assets are fetched only when needed.

## Anti-patterns

- **Committing a big file "just this once."** It's now in history; the fix is a history rewrite.
- **Using LFS without a plan for quotas and access.** Bandwidth and storage limits turn into surprise failures on CI or for forks.
- **Versioned filenames** like `model_v3_final.pt` in git or storage. Use tags and manifests (see `versioning-in-paths`).
- **Assets with no fetch instructions.** A pointer nobody can resolve is a broken repository.
- **Binary artifacts checked in to avoid building them.** Publish builds to a registry instead.
- **Mixing raw inputs with regenerated data** in one directory (see `stable-vs-volatile-separation`).

## Scaling & failure modes

- **Storage growth**: large-file storage costs accumulate; set retention and delete unreferenced objects.
- **Team access**: object storage and LFS need credentials; document how contributors get access, and avoid embedding keys in the repo.
- **CI time**: fetching large assets on every run is slow; cache them keyed by manifest hash.
- **Diffs and merges**: binaries can't be merged; use file locking (`git lfs lock`) for assets that people edit.
- **Provenance**: for datasets, record source, date, and license next to the manifest so results can be reproduced later.

## Variants

- **Plain git for small assets**: fine below a few megabytes total.
- **Git LFS**: pointer files in git, blobs on an LFS server; good for design assets and media edited by hand.
- **DVC (or similar)**: pointers to remote storage plus pipeline definitions; good for datasets and model artifacts.
- **Object storage plus manifest**: a bucket and a checked-in manifest with hashes; the simplest portable option.
- **Artifact registry**: build outputs published to a package or container registry, consumed by version.
- **git-annex**: distributed large-file management for people who need multiple remotes.

## Adoption checklist

- [ ] `git count-objects -vH` shows a size you're comfortable cloning.
- [ ] Every large-asset directory is covered by LFS, DVC, or an external store.
- [ ] The README says exactly how to fetch the large files.
- [ ] A manifest with `sha256` hashes exists and is checked in CI.
- [ ] Generated binaries are not committed.
- [ ] Access and retention for the storage backend are documented.

## Real-world projects using this

- **Git LFS** (git-lfs.com), created by GitHub and Atlassian, is documented with the pointer-file model and `git lfs migrate`.
- **DVC** (dvc.org) documents data and model versioning with pointer files and remotes for machine-learning projects.
- **git-annex** is a long-standing tool for managing large files across multiple repositories.
- **Hugging Face** hosts models and datasets as git repositories that use LFS-style storage for large files.
- **BFG Repo-Cleaner** and **`git filter-repo`** document history rewriting for removing large blobs.

## Migration & references

- **From plain git with big files:** use `git lfs migrate import` (or `git filter-repo` plus DVC) on a mirror clone, force-push after agreement, and have contributors re-clone.
- **From ad-hoc shared drives:** move files to object storage, generate a manifest, and add a fetch script.
- **Between backends:** the manifest is the contract; write a script that fetches by hash from the new store and verifies.
- **References:**
  - `principles/generated-vs-source-separation/` and `principles/stable-vs-volatile-separation/` for what to keep out of git.
  - `code/cookiecutter-data-science/` and `code/ml-experiment-project/` for data and model layouts.
  - `files/backup-3-2-1-layout/` for backing up what git should not hold.

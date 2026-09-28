# Project

## Fetching large files

The repository keeps only pointers to large files.

```bash
git lfs install
git lfs pull
sha256sum -c assets/media/media.manifest
```

Datasets are versioned with DVC: run `dvc pull` after configuring the remote (see `docs/data.md`).

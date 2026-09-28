# large-files-and-binary-assets — canonical tree

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

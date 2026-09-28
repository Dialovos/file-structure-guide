# git-worktrees-layout — canonical tree

```
Sibling layout (recommended):

projects/
├── myapp/                         ← main checkout (usually main)
│   ├── .git/                      ← the real repository
│   └── src/
└── myapp.worktrees/               ← every extra worktree lives here
    ├── feature-login/             ← branch feature/login
    ├── fix-timeout/               ← branch fix/timeout
    └── review-pr-482/             ← temporary, for reviewing a pull request

In-repository layout (alternative):

myapp/
├── .git/
├── .gitignore                     ← contains `.worktrees/`
├── .worktrees/                    ← gitignored
│   └── feature-login/
└── src/

Bare-repository layout (advanced):

myapp/
├── .bare/                         ← bare repository
├── .git                           ← file pointing to .bare
├── main/                          ← worktree
└── feature-login/                 ← worktree
```

# unix-fhs — canonical tree

```
/
├── etc/                ← host-specific config
├── usr/
│   ├── bin/            ← shipped binaries
│   ├── local/          ← admin-installed (your stuff)
│   └── share/          ← arch-independent data
├── var/
│   ├── log/            ← log files
│   ├── lib/            ← persistent state
│   └── cache/
├── home/<user>/
├── opt/<vendor>/       ← third-party self-contained
└── srv/<service>/      ← service-served data
```

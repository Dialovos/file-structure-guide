# monorepo-vs-polyrepo — canonical tree

```
monorepo (single owner, ships together)/
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   ├── shared-types/
│   └── ui/
└── README.md

polyrepo (independent owners and cadences)/
├── acme-sdk/            ← own repo, own releases
├── acme-web/            ← own repo, depends on acme-sdk by version
└── acme-infra/          ← own repo, restricted access

hybrid/
├── acme-platform/       ← monorepo: api, worker, shared packages
└── acme-sdk/            ← separate repo: public, semver'd
```

# 00.00 Johnny Decimal index

The canonical map of this vault. Every area, category, and item is listed here. Maintain it by hand; it is the system, the IDs alone are not.

## Areas

| Range | Area    | Status        |
| ----- | ------- | ------------- |
| 00-09 | system  | meta files, this index, and any vault-level docs |
| 10-19 | life    | personal life: home, health, finance, family     |
| 20-29 | work    | professional life: clients, projects, employer  |

> Add new areas only when an existing one cannot accommodate a new category at all. Aim for headroom — ten areas total is the cap, not the target.

## Categories

### 00-09 system

| ID | Name  | Notes                       |
| -- | ----- | --------------------------- |
| 00 | index | this file lives at 00.00    |

### 10-19 life

| ID | Name    | Notes                              |
| -- | ------- | ---------------------------------- |
| 11 | home    | lease, utilities, household admin  |
| 12 | health | medical records, prescriptions, GP |

### 20-29 work

| ID | Name      | Notes                  |
| -- | --------- | ---------------------- |
| 21 | client-a | first major client     |

## Sample item naming

```
10-19 life/
└── 11 home/
    ├── 11.01 lease.md
    └── 11.02 utility-bills.md
```

The two-part ID (`11.01`) is the durable name; the human suffix (`lease.md`) can change without breaking the ID.

## Rules cheat-sheet

- 10 areas max. 10 categories per area max. 99 items per category max.
- Two levels only — area, then category. Items go directly inside categories.
- IDs are immutable once assigned; retire, do not recycle.
- This index is the source of truth — every new category and item gets a row here at creation time.

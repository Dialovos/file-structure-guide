# terraform-infrastructure — canonical tree

```
infra/
├── modules/
│   ├── network/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf                  ← composes modules
│   │   ├── backend.tf               ← remote state for dev only
│   │   ├── versions.tf              ← required_version, required_providers
│   │   ├── variables.tf
│   │   ├── terraform.tfvars         ← non-secret inputs
│   │   └── .terraform.lock.hcl      ← committed
│   └── prod/
│       └── (same shape)
├── .gitignore                       ← .terraform/, *.tfstate*, secret tfvars
└── README.md
```

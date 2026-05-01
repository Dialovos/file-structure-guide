```
mysite/
├── manage.py
├── pyproject.toml
├── mysite/                     ← project config package
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tests/
│   │   └── migrations/
│   └── billing/
├── static/
├── templates/
├── media/                      ← gitignored
└── requirements/
    ├── base.txt
    ├── dev.txt
    └── prod.txt
```

## TL;DR

Django ships with a usable project layout from `django-admin startproject`, but the moment your project grows past a single app you want the **app-per-feature layout** popularized by *Two Scoops of Django* and `cookiecutter-django`. The shape: `manage.py` at the root, a project-config package (`mysite/`) holding `settings/` (split into `base.py`, `dev.py`, `prod.py`), `urls.py`, `wsgi.py`, `asgi.py`. Apps live as siblings under `apps/<feature>/`. `requirements/` is split into `base.txt`, `dev.txt`, `prod.txt`. Templates and static files live at the repo root in `templates/` and `static/`. This layout scales from a hobby project to a multi-team Django service without restructuring. The two non-default moves are (1) `settings/` as a package not a file, (2) apps under `apps/` with full dotted names like `apps.accounts`. Both pay off the second you add a second environment or a second team.

## Principles & why

Django's defaults assume one app. Real Django projects don't have one app. This layout names that gap explicitly.

1. **Split settings.** A single `settings.py` is a footgun the moment you have a dev DB and a prod DB. The `settings/` package with `base.py` (shared), `dev.py` (overrides for local), and `prod.py` (overrides for prod, env-driven) makes environment differences explicit and grep-able. `DJANGO_SETTINGS_MODULE=mysite.settings.dev` is your one knob. *Two Scoops of Django* established this convention; it has held up for a decade.
2. **Apps under `apps/`.** Putting apps at the repo root works, but it floods the top level with `accounts/`, `billing/`, `analytics/`, `core/` next to `mysite/`, `templates/`, `static/`, and `manage.py`. With `apps/` as a container, the root reads as "one Django site," and apps are clearly second-order.
3. **Apps imported with full dotted paths.** `apps.accounts` not `accounts`. This requires `apps/__init__.py` and `name = "apps.accounts"` in each app's `apps.py` — a one-time setup that makes `INSTALLED_APPS` self-documenting.
4. **Environment-specific requirements.** `requirements/base.txt` declares everything the app needs to *run*. `dev.txt` adds tools for local work (debug toolbar, pytest, ipython). `prod.txt` adds gunicorn, psycopg, Sentry. The `-r base.txt` chain keeps base in one place.
5. **`media/` is gitignored, `staticfiles/` is gitignored.** `static/` (sources) is committed. `media/` (uploads) and `staticfiles/` (collectstatic output) are not. This split is canonical Django.

The principle underneath: every Django project has *layers* (config, apps, templates, static, requirements). The layout makes each layer addressable, so a new contributor can locate any concern in 30 seconds.

## When to use

- **Any Django project larger than a single app.** Even two apps benefit; the cost is one extra directory.
- **Multi-environment deploys.** Dev, staging, prod settings diverge in real ways (DEBUG, allowed hosts, DB, cache). Settings split is mandatory.
- **Multi-developer teams** where settings, requirements, and apps are touched by different people.
- **Projects that will live more than 6 months.** The layout absorbs growth (more apps, more envs, more requirements layers) without restructuring.
- **Teams adopting `cookiecutter-django` or *Two Scoops* conventions.** This guide *is* those conventions, distilled.

## When NOT to use

- **Tutorial Django apps and one-page demos.** `django-admin startproject` is fine; don't manufacture structure for a 50-line view.
- **Headless API-only services where Django is already overkill.** Consider `code/fastapi-project/` instead — FastAPI is lighter for pure JSON APIs.
- **Single-app Django projects** where you genuinely will never add a second app. (Be honest; "I'll add more apps later" is how single-app projects acquire more apps.)
- **CMS-driven projects** (Wagtail, Mezzanine) which often impose their own layout conventions on top of Django. Follow the CMS's layout.
- **Microservices with one model and one endpoint.** Django's batteries-included ergonomics get expensive at small sizes.

## Tree diagram

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

## Naming rules

- **Project config package**: `snake_case`, often matching the project name (`mysite/`, `acme/`). Required because the directory is the Python import path.
- **Apps**: `snake_case`, descriptive of feature, not type — `accounts/`, `billing/`, `posts/`, *not* `models/` or `views/`. (Type-based naming is a known Django anti-pattern; see `principles/naming-by-purpose-not-type/`.)
- **App's `apps.py`** declares `name = "apps.accounts"` — full dotted path with `apps.` prefix. Required so Django's app registry sees the right name.
- **Settings filenames**: `base.py`, `dev.py`, `prod.py`, optionally `staging.py`, `test.py`. Lowercase, no underscores.
- **Requirements files**: `base.txt`, `dev.txt`, `prod.txt`. Same convention.
- **Templates**: per-app templates live in `apps/<app>/templates/<app>/file.html` (the doubled name is a Django convention to avoid template-namespace collisions). Site-wide templates live in repo-root `templates/`.
- **URL include names**: dotted path in `urls.py` — `path("accounts/", include("apps.accounts.urls"))`.

## Worked example

A single `settings.py` has `DEBUG = True` toggled by commenting, and one app named `core` holds 40 models.

1. Split settings: `mysite/settings/base.py`, `dev.py`, `prod.py`. `dev.py` and `prod.py` start with `from .base import *`.
2. Point `manage.py`, `wsgi.py`, and `asgi.py` at `mysite.settings.dev` by default and select `prod` with `DJANGO_SETTINGS_MODULE`.
3. Read secrets from the environment (`SECRET_KEY = os.environ["SECRET_KEY"]`) and list variable names in `.env.example`.
4. Split `core` into apps by feature under `apps/` (`accounts`, `billing`); update `INSTALLED_APPS` to `apps.accounts`, and set `name = "apps.accounts"` in each `apps.py`.
5. Use `makemigrations --check --dry-run` in CI to catch missing migrations.

Each app now owns its models, views, URLs, and tests, and environments differ in one small file.

## Anti-patterns

- **A single `settings.py` with `if DEBUG:` branches.** Settings files should be flat data plus a small amount of import logic, not branching. Split into a package.
- **`from .settings import *` followed by overrides at the bottom of `settings.py`.** This was the pre-package convention; the package layout is cleaner.
- **Apps named after types.** `models/`, `views/`, `helpers/` at the apps level. An app is a feature; `accounts/`, `billing/` are right.
- **Hardcoded secrets in `settings/base.py`.** Use environment variables (`os.environ` or `django-environ`) loaded in `prod.py`, with a placeholder in `base.py`.
- **`requirements.txt` as one giant file.** Splits into `base/dev/prod` are five lines of work and prevent dev-only packages from being installed in production.
- **Apps importing each other in undocumented ways.** Dependencies between apps should be one-directional and explicit. If `apps.billing` imports from `apps.accounts.models`, document it; if it's bidirectional, you have one app pretending to be two.
- **`media/` committed to git.** User uploads are not source. Gitignore them; back them up separately.
- **`staticfiles/` committed.** That's `collectstatic` output, not source. Gitignore.

## Scaling & failure modes

- **Circular imports between apps** signal that apps are too fine-grained or coupled through models. Use string references (`"billing.Invoice"`) for foreign keys and signals or services for behavior.
- **Migrations** accumulate. Squash after releases, and never edit an applied migration.
- **Fat models and fat views**: move multi-model logic into `services.py` or `selectors.py` inside the app.
- **Settings sprawl**: past three environments, consider `django-environ` or `pydantic-settings` over subclass files.

## Variants

- **apps-flat** — apps at the repo root next to `mysite/`, no `apps/` container. Smaller projects can do this. The cost is a noisier root; the benefit is one fewer level of `apps.` dotted prefixes.
- **settings-as-single-file** — for very small projects, keep `settings.py` and use environment variables for the only differences. Migrate to `settings/` package when you have ≥3 environment-specific differences.
- **12-factor-env-only** — no `dev.py`/`prod.py`; one `settings.py` reads everything from environment variables (`DJANGO_DEBUG`, `DATABASE_URL`, etc.). Common in container deploys; loses the readability of settings-as-Python.
- **Django REST Framework layout** — same shape, plus `apps/<app>/serializers.py` and `apps/<app>/api.py`. Compatible with this guide.
- **Wagtail / Mezzanine** — CMS-imposed layouts; usually a layer on top of this one.
- **`src/` layout for Django** — uncommon but works; `manage.py` stays at the root, project package and apps go under `src/`. Adds the src-layout discipline (see `code/python-src-layout/`) at the cost of an extra directory level.

## Adoption checklist

- [ ] `python manage.py check --deploy --settings=mysite.settings.prod` passes with the production environment.
- [ ] `makemigrations --check` is clean in CI.
- [ ] No secrets in tracked settings; `.env.example` lists all variables.
- [ ] Each app has its own `tests/` and does not import another app's private modules.
- [ ] `media/` and collected static output are gitignored.

## Real-world projects using this

- **`cookiecutter-django`** — the canonical opinionated Django starter; this guide is essentially its layout, simplified.
- ***Two Scoops of Django*** (Daniel & Audrey Roy Greenfeld) — the book that established split-settings and `apps/` as conventions.
- **Django REST Framework example projects** — most use this shape with serializer/api additions.
- **Mozilla's older open-source Django sites** (Kuma, Mozillians) — pioneered split-settings before the cookiecutter formalised it.
- **Many Y Combinator and OSS Django projects** — Sentry (early days), Mailtrain, taiga.io, Zulip's web frontend (Django-flavored backend).
- **Django docs' "deployment" page** still recommends environment-specific settings; cookiecutter codifies the recommendation.

## Migration & references

- **From `django-admin startproject` default**: create `mysite/settings/`, move `settings.py` content into `mysite/settings/base.py`, add `dev.py` and `prod.py` with `from .base import *` plus overrides. Update `manage.py`, `wsgi.py`, `asgi.py` to default to `mysite.settings.dev`. Update CI to set `DJANGO_SETTINGS_MODULE=mysite.settings.prod` for deploys.
- **From apps-at-root to apps-under-`apps/`**: `mkdir apps && git mv accounts billing posts apps/`. Update `INSTALLED_APPS` to use `apps.accounts` etc., update each app's `apps.py` to set `name = "apps.<app>"`. Update `urls.py` includes. Run the test suite.
- **From `requirements.txt` monolith**: create `requirements/base.txt` with everything that runs in production, `requirements/dev.txt` starting with `-r base.txt` and adding dev tools, `requirements/prod.txt` starting with `-r base.txt` and adding deploy tools. Delete the old `requirements.txt`.
- **References**:
  - *Two Scoops of Django* (Greenfeld & Greenfeld) — the canonical reference.
  - `cookiecutter-django` repo and docs — the living implementation.
  - Django docs, "Deploying Django" and "Settings" sections.
  - Sibling guides: `code/python-flat-layout/` (the underlying Python layout shape), `code/fastapi-project/` (when Django is overkill), `principles/naming-by-purpose-not-type/` (apps named for features, not file types), `principles/stable-vs-volatile-separation/` (why split settings).

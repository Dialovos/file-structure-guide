# Django project — template

A `cp -r`-able starter for a multi-app Django site using the
*Two Scoops* / `cookiecutter-django` conventions: split settings,
apps under `apps/`, environment-specific requirements.

## What to rename

- `mysite/` (project config package) → `<your_site>/` everywhere it
  appears: directory name, `manage.py`, `wsgi.py`, `asgi.py`,
  `pyproject.toml`, every `mysite.settings.*` reference.
- `apps/example_app/` → your real first app. Update its
  `apps.py` (`name = "apps.<your_app>"`), `urls.py`, models, views.
- Update `mysite/settings/base.py` `INSTALLED_APPS` to list your app.
- Update `mysite/urls.py` to include your app's URLConf.

## What to fill

- **`mysite/settings/prod.py`** — hardcoded *names* are fine, but
  every secret must come from environment variables. Sample env file
  belongs in `.env.example` (not committed).
- **`pyproject.toml`** — name, description, authors, dependencies.
- **`requirements/*.txt`** — pin versions as you add deps. Keep
  `base.txt` minimal; `dev.txt` and `prod.txt` extend it.
- **`LICENSE`** — replace `{{YEAR}}` and `{{NAME}}`, or pick another.
- **`apps/example_app/models.py`** — replace `Note` with real models.

## What to delete

- `apps/example_app/` once you have your own first app.
- This `README.md` once you have a real one.

## First run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/example/` to confirm the example app is
wired up. Visit `/admin/` after running `createsuperuser`.

## Production setup (sketch)

```bash
export DJANGO_SETTINGS_MODULE=mysite.settings.prod
export DJANGO_SECRET_KEY=<strong-random-value>
export DJANGO_ALLOWED_HOSTS=example.com,www.example.com
export POSTGRES_DB=mysite
export POSTGRES_USER=mysite
export POSTGRES_PASSWORD=<secret>
pip install -r requirements/prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn mysite.wsgi:application
```

## Pair this with

- `../GUIDE.md` — the full reasoning behind the layout.
- `../../python-flat-layout/` — the underlying Python layout shape.
- `../../fastapi-project/` — when Django is overkill for an API.
- `../../../principles/naming-by-purpose-not-type/` — apps named
  for features, not file types.
- `../../../principles/stable-vs-volatile-separation/` — why split
  settings.

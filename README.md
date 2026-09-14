# Affordable Housing Price Estimator

A Django web application that uses the committed `affordable_price_model.pkl`
regression model to estimate affordable housing prices in Kenyan shillings.

## Application structure

- `manage.py` identifies the Django project for local development and Vercel.
- `housing_estimator/wsgi.py` is the production WSGI entrypoint.
- `predictor/` contains the form, views, and prediction service.
- `templates/` and `static/` contain the web interface.
- `.python-version` pins the Vercel runtime to Python 3.12.
- `.vercelignore` keeps notebooks, training data, and local artifacts out of the
  production deployment while retaining the trained model.

## Local setup

Create and activate a virtual environment, then install the runtime dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python manage.py runserver 127.0.0.1:8001
```

Open:

- Landing page: `http://127.0.0.1:8001/`
- Prediction page: `http://127.0.0.1:8001/predict/`
- Health check: `http://127.0.0.1:8001/health/`

Run the automated checks with:

```powershell
python manage.py check
python manage.py test
```

The optional notebook and Streamlit dependencies remain in
`requirements-dev.txt`; they are not installed in production.

## Vercel deployment

Vercel supports Django directly. It detects `manage.py`, resolves
`housing_estimator.wsgi.application`, runs `collectstatic`, and serves the
collected assets from its CDN. No custom Build Command, Output Directory,
Install Command, `/api` wrapper, or legacy `builds`/`routes` configuration is
needed.

### 1. Import the GitHub repository

1. Sign in to [Vercel](https://vercel.com/) with the GitHub account that can
   access this repository.
2. Select **Add New > Project**.
3. Import `JAPHES/Affordable-housing-price-estimator`.
4. Leave **Root Directory** at the repository root (`./`).
5. Keep the automatically detected Python/Django build settings. Do not enter a
   custom Build Command, Output Directory, Install Command, or Start Command.

### 2. Add the required environment variable

Generate a secret locally:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

In the Vercel project's **Settings > Environment Variables**, add the generated
value as:

```text
SECRET_KEY=<the-generated-value>
```

Apply it to **Production**, **Preview**, and **Development**. Do not commit the
secret to Git.

Vercel system environment variables must remain enabled (the default for new
projects). The Django settings use `VERCEL`, `VERCEL_URL`,
`VERCEL_BRANCH_URL`, and `VERCEL_PROJECT_PRODUCTION_URL` to disable debug mode
and accept generated, preview, and production domains automatically.

### 3. Deploy and verify

Select **Deploy**. After the deployment is ready, verify these paths on the
generated `vercel.app` domain:

- `/` renders the landing page.
- `/predict/` accepts the form and returns an estimated price.
- `/health/` returns `{"status": "ok"}`.
- `/static/predictor/styles.css` returns the stylesheet.

Future pushes to `main` will create production deployments automatically once
the Git repository is connected to the Vercel project.

### Optional custom domains

The primary Vercel production domain is accepted automatically. If the project
uses additional custom-domain aliases, add these comma-separated variables and
redeploy:

```text
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
```

This application currently does not use persistent database-backed features.
If that changes, connect a managed database rather than relying on the local
SQLite file in a Vercel Function.

See Vercel's current [Django deployment guide](https://vercel.com/docs/frameworks/full-stack/django)
and [system environment variable reference](https://vercel.com/docs/environment-variables/system-environment-variables)
for platform details.

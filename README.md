# Affordable Housing Price Estimator

Django web app for the existing `affordable_price_model.pkl` housing price model.

## Local Run

```powershell
python manage.py runserver 127.0.0.1:8001
```

Landing page:

```text
http://127.0.0.1:8001/
```

Prediction page:

```text
http://127.0.0.1:8001/predict/
```

## Railway Deployment

This project includes `railway.json`, so Railway will:

- build with Railpack
- run `python manage.py collectstatic --noinput`
- start the app with Gunicorn on Railway's `$PORT`
- healthcheck `/`

Required Railway variables:

```text
SECRET_KEY=<generate a strong Django secret>
DEBUG=False
```

Optional variables:

```text
DJANGO_ALLOWED_HOSTS=your-custom-domain.com
CSRF_TRUSTED_ORIGINS=https://your-custom-domain.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

Railway provides `PORT` and `RAILWAY_PUBLIC_DOMAIN` automatically for the app service.

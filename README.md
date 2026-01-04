# lost_and_found_app

Deployment
----------

Recommended: use Render (https://render.com) for a simple deploy of this Django app.

Quick steps (Render):
1. Create a free account at render.com and connect your GitHub repository.
2. Create a **Web Service** and choose this repository.
   - Environment: **Python 3**
   - Build Command: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn core.wsgi --bind 0.0.0.0:$PORT`
3. Set environment variables in Render:
   - `DJANGO_SECRET_KEY` (keep it secret)
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` = `example.com` (set to your render service domain)
   - Database: add a managed Postgres and set `DATABASE_URL` in env (Render provides this)
4. Push to the `main` branch. You can also use the provided GitHub Action `deploy-to-render.yml` which triggers a Render deploy when pushed to `main`. Make sure to set repository secrets `RENDER_SERVICE_ID` and `RENDER_API_KEY`.

Alternative: Use other providers (Railway, Fly.io, Heroku) — the project includes a `Procfile` and `runtime.txt` for Heroku-like deployments.

Security
--------
Make sure you set a strong `DJANGO_SECRET_KEY` in production and set `DJANGO_DEBUG` to `False`.

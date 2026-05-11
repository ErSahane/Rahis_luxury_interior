# Rahis Luxury Interiors

A full-stack Django website for a luxury furniture and interior business.

## Features

- Premium responsive homepage with hero image slider, glassmorphism, animation, counters, reviews, before/after comparison, dark/light mode, WhatsApp, and click-to-call.
- Dynamic portfolio gallery with categories and fullscreen lightbox.
- Appointment booking form saved to SQLite.
- Custom secure dashboard for analytics, project CRUD, multiple image upload, appointment status, delete, and CSV export.
- Django admin support for services, projects, appointments, testimonials, and gallery images.

## Local Run

```powershell
& "C:\Users\Sahane alam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" manage.py runserver 127.0.0.1:8000
```

Open:

- Website: `http://127.0.0.1:8000/`
- Custom dashboard: `http://127.0.0.1:8000/dashboard/login/`
- Django admin: `http://127.0.0.1:8000/admin/`
- FastAPI docs, after starting the API server: `http://127.0.0.1:9000/docs`

Local dashboard login:

- Username: `admin`
- Password: `Rahis@2026`

## Production Notes

Set these environment variables before deployment:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`

The default database is SQLite. For MySQL, update `DATABASES` in `rahis_luxury/settings.py` and install the preferred MySQL driver.

## FastAPI Server

FastAPI is included as a separate API app in `fastapi_app.py`. Install the requirements, then run:

```powershell
& "C:\Users\Sahane alam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m uvicorn fastapi_app:app --host 127.0.0.1 --port 9000 --reload
```

Available endpoints:

- `GET /api/health`
- `GET /api/services`
- `GET /api/projects`
- `GET /api/projects?category=kitchen`
- `GET /api/projects/{project_id}`
- `POST /api/appointments`
- `GET /api/testimonials`

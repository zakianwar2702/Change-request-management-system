Django support dashboard scaffold

Quick start (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements

```powershell
pip install -r requirements.txt
```

3. Run migrations and start the server

```powershell
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the support dashboard.

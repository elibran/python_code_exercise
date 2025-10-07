# FastAPI + SQLite (Dev)

## 1) Activate venv and install deps
```powershell
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2) Run the API
```powershell
setx DATABASE_URL "sqlite:///./dev.db"
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API (POST /tasks, GET /tasks).

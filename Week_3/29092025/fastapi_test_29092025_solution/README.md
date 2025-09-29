# Clinic Slots API — Coding Test

## Setup
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run (optional)
```bash
uvicorn app.main:app --reload
```

## Tests
```bash
python -m pytest -q tests/student
# (Instructor suite)
python -m pytest -q tests/instructor
```

### Using the reference solution
To replace the starter `app/` with the reference implementation:
```bash
python scripts/use_solution.py
```
This will copy `solution/app` over `app`.

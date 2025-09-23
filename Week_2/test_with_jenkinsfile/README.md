# Personal Banking — Simple Demo, Tests & CI

This repository contains a **tiny, intentionally simple** Python package that models:
- an `Account` with `deposit`, `withdraw`, and `get_balance`,
- a loan decision helper that approves/rejects using a mock score,
- a currency conversion helper used by an *international transfer* demo.

The code emphasizes **clarity over cleverness**, small functions, and explicit errors.
Docstrings are provided throughout to improve readability and discoverability.

## Project layout
```text
personal-banking/
  banking/
    __init__.py
    account.py        # Simple Account
    loans.py          # Mock scoring + loan decision
    transfers.py      # FX lookup + conversion helper
  tests/
    test_*.py         # Pytest unit tests
  Jenkinsfile         # Jenkins pipeline (Windows + macOS/Linux)
  requirements.txt
  README.md
```

---

## Quickstart

### 1) Create & activate a virtual env

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux (bash/zsh):**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run tests (with coverage & JUnit XML)
```bash
pytest -q --cov=banking --cov-report=term-missing --cov-report=xml:reports/coverage.xml --junitxml=reports/junit.xml
```

### 4) Deactivate the virtual env
**Windows (PowerShell):**
```powershell
deactivate
```

**macOS / Linux:**
```bash
deactivate
```

---

## Design notes

* Keep functions small and predictable.
* Validate inputs early and raise *clear* `ValueError` where appropriate.
* Push I/O to the edges: `transfers.get_exchange_rate` is the only place that reaches out
  to the network and is wrapped with a friendly `ExchangeRateError` so callers can handle it.
* Tests patch dependencies (e.g., `check_credit_score`, `get_exchange_rate`) to stay fast and deterministic.

---

## Local testing recipes

**Fast run:**
```bash
pytest -q
```

**With coverage summary + artifacts in `reports/`:**
```bash
pytest -q --cov=banking --cov-report=term-missing --cov-report=xml:reports/coverage.xml --junitxml=reports/junit.xml
```

**Run a single test file:**
```bash
pytest -q tests/test_account.py
```

**Run a single test case (node id):**
```bash
pytest -q tests/test_account.py::test_deposit_increases_balance
```

---

## Jenkins pipeline (Windows + macOS/Linux)

The provided **Declarative** `Jenkinsfile` auto-detects the agent OS and uses the appropriate commands.

**Stages:**
1. *Checkout* – default SCM checkout.
2. *Setup Python* – prints interpreter info for debugging agents.
3. *Install deps* – creates a virtualenv and installs pinned deps.
4. *Test* – runs pytest with coverage and outputs JUnit + coverage XML into `reports/`.
5. *Post* – publishes JUnit results, archives reports, and always cleans the workspace.

**Artifacts & reports produced:**
- `reports/junit.xml` – JUnit test results (consumed by `junit` step).
- `reports/coverage.xml` – coverage report (you can add Cobertura/JaCoCo publishers if desired).

---

## Beginner-Friendly Jenkins on Windows (Step by Step)

### 1. Install prerequisites
- **Jenkins (LTS)** → run the Windows installer → open <http://localhost:8080> → complete setup.
- **Git for Windows** (ensure “Add Git to PATH” checked).
- **Python 3.x** (ensure “Add to PATH” checked).
- Verify in Command Prompt:
  ```cmd
  python --version
  pip --version
  git --version
  ```
- (Optional) If PowerShell blocks venv activation:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### 2. Make repo available
Push your project to GitHub/GitLab/Bitbucket, or have Jenkins point to a local Git repo.

### 3. Create a Pipeline job in Jenkins
1. Jenkins dashboard → **New Item** → name: `personal-banking` → choose **Pipeline**.
2. Under **Pipeline**:
   - Definition: *Pipeline script from SCM*
   - SCM: *Git*
   - Repo URL: your repo URL
   - Script Path: `Jenkinsfile`
3. Save.

### 4. Run the pipeline
- Click **Build Now**.
- Stages run automatically:
  - Checkout → Setup Python → Install deps → Test → Post.
- Reports and test results appear in the build summary.

### 5. Where to see results
- **Test Result** link in build page.
- **Artifacts** (in left menu): open `reports/coverage.xml` and `reports/junit.xml`.
- **Console Output**: shows real-time pipeline logs.

### 6. Common Windows gotchas
- *python not found*: Reinstall Python with PATH enabled.
- *venv activate blocked*: Run `Set-ExecutionPolicy` as shown above.
- *pip behind proxy*: configure pip with `--proxy` option.
- *Multiple Python installs*: ensure the correct Python is first in PATH.

### 7. Optional sanity check
If build fails early, temporarily add this stage in Jenkinsfile:

```groovy
stage('Sanity check') {
  steps {
    bat '''
      where python
      python --version
      pip --version
      where git
    '''
  }
}
```

---

## Troubleshooting

* **SSL/network issues during FX lookup:** tests **mock** the network call;
  if you run the function manually without internet, you'll get `ExchangeRateError`.
* **Windows PowerShell execution policy blocks venv activation:** run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`,
  then re-open PowerShell.
* **Multiple Python versions:** ensure `python`/`python3` is the one with `venv` module available.

---

## Extending this demo

* Replace the FX API with your internal service and adapt `get_exchange_rate` accordingly.
* Swap out the loan approval logic for a rules engine or model – tests will still patch the score provider.
* Introduce persistence (DB) by adding a repository layer; keep `Account` pure and easy to test.

"""
This README intentionally includes both Windows and macOS/Linux commands to make the
code and pipeline runnable on common developer setups and CI agents.
"""

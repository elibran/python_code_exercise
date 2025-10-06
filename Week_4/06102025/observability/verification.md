

---

## 🧪 Detailed Pytest Reporting Options

You can run pytest with different levels of verbosity and reporting based on your needs:

### 1️⃣ Verbose output (show all tests)
```bash
pytest -v
```

### 2️⃣ Show print/log output too
```bash
pytest -v -s
```
> Useful when debugging or checking JSON log formatting and correlation IDs.

### 3️⃣ Show slowest tests
```bash
pytest -v --durations=10
```
> Lists the 10 slowest tests for performance insights.

### 4️⃣ Very verbose with detailed tracebacks
```bash
pytest -vv --maxfail=3 --tb=long
```
> Displays full tracebacks and stops after 3 failed tests.

### 5️⃣ Generate XML or HTML reports

**JUnit XML report (for CI/CD integration):**
```bash
pytest -v --junitxml=report.xml
```

**HTML report (for rich, human-readable output):**
```bash
pip install pytest-html
pytest -v -s --durations=10 --html=pytest-report.html --self-contained-html
pytest -v -s --html=pytest-report.html --self-contained-html

```
> The HTML report includes full details, captured logs, durations, and pass/fail summaries.


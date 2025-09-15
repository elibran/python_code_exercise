# 🚀 Python 3.11.7 Installation & VS Code Development Environment Setup

This guide provides **step-by-step instructions** to install **Python 3.11.7** and prepare a **complete development environment** using **Visual Studio Code (VS Code)**.  
The steps are written in **incremental fashion** – start from the basics and move toward a ready-to-code environment.

---

## 1️⃣ Install Python 3.11.7

### Windows
1. Go to the official Python downloads page:  
   👉 [Python 3.11.7 for Windows](https://www.python.org/downloads/release/python-3117/)
2. Download the **Windows installer (64-bit)**.
3. Run the installer:
   - ✅ Check **"Add Python 3.11 to PATH"**
   - Select **Customize Installation** → Keep all default options checked.
   - Choose **Install for all users** (recommended).
4. Verify installation:
   ```powershell
   python --version
   ```
   Should output:
   ```
   Python 3.11.7
   ```

---

### macOS
1. Install **Homebrew** (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python 3.11.7:
   ```bash
   brew install python@3.11
   ```
3. Ensure `python3.11` points correctly:
   ```bash
   brew link python@3.11 --force
   ```
4. Verify installation:
   ```bash
   python3.11 --version
   ```
   Output should be:
   ```
   Python 3.11.7
   ```

---

### Linux (Ubuntu/Debian)
1. Update system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Install prerequisites:
   ```bash
   sudo apt install -y build-essential libssl-dev zlib1g-dev    libncurses5-dev libffi-dev libsqlite3-dev libreadline-dev wget curl
   ```
3. Download Python 3.11.7 source:
   ```bash
   wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz
   ```
4. Extract and build:
   ```bash
   tar -xvzf Python-3.11.7.tgz
   cd Python-3.11.7
   ./configure --enable-optimizations
   make -j$(nproc)
   sudo make altinstall
   ```
5. Verify installation:
   ```bash
   python3.11 --version
   ```
   Output:
   ```
   Python 3.11.7
   ```

---

## 2️⃣ Set Up Virtual Environment (Recommended for Projects)

1. Create a project folder:
   ```bash
   mkdir my_python_project && cd my_python_project
   ```
2. Create a virtual environment:
   ```bash
   python3.11 -m venv venv
   ```
3. Activate the environment:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
4. Confirm:
   ```bash
   which python
   ```
   Should point to your project `venv`.

---

## 3️⃣ Install VS Code

1. Download and install **Visual Studio Code**:  
   👉 [VS Code Download](https://code.visualstudio.com/Download)

2. Install the following **extensions**:
   - 🟦 Python (`ms-python.python`)
   - 🟦 Pylance (`ms-python.vscode-pylance`)
   - 🟦 Jupyter (`ms-toolsai.jupyter`) – optional, for notebooks
   - 🟦 Black Formatter (`ms-python.black-formatter`) – optional, for code style

---

## 4️⃣ Configure VS Code for Python

1. Open your project folder in VS Code:
   ```bash
   code my_python_project
   ```
2. Select Python interpreter:
   - Press **Ctrl+Shift+P** (or Cmd+Shift+P on macOS).
   - Search for **Python: Select Interpreter**.
   - Choose the one from your **venv**.
3. Create a file `app.py`:
   ```python
   print("Hello, Python 3.11.7 with VS Code!")
   ```
4. Run with:
   ```bash
   python app.py
   ```

---

## 5️⃣ Install Developer Essentials

Inside your virtual environment, install common packages:

```bash
pip install --upgrade pip
pip install black flake8 pytest requests
```

- **black** → automatic code formatting  
- **flake8** → linting  
- **pytest** → testing framework  
- **requests** → common HTTP library  

---

## 6️⃣ (Optional) Set Up Debugging in VS Code

1. Go to **Run & Debug** (Ctrl+Shift+D).
2. Click **Create a launch.json file**.
3. Choose **Python file**.
4. Add breakpoints and press **F5** to debug.

---



---

## 7️⃣ Set Up Git & GitHub Access

### Windows (Git Bash)
1. Download Git for Windows:  
   👉 [Git for Windows](https://git-scm.com/download/win)
2. Install using default options. This will include **Git Bash** (a terminal that works like Linux).
3. Open **Git Bash** and configure Git:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```
4. Generate SSH key (for secure GitHub access):
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```
   Press Enter to accept defaults.
5. Add your SSH key to GitHub:
   - Copy key:
     ```bash
     cat ~/.ssh/id_ed25519.pub
     ```
   - Go to **GitHub → Settings → SSH and GPG keys → New SSH key**, paste the key, and save.
6. Test the connection:
   ```bash
   ssh -T git@github.com
   ```

### macOS / Linux
1. Install Git (if not already installed):
   ```bash
   sudo apt install git -y          # Ubuntu/Debian
   brew install git                 # macOS (Homebrew)
   ```
2. Configure Git:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```
3. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```
4. Add SSH key to GitHub:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Copy and paste into **GitHub → Settings → SSH and GPG keys → New SSH key**.
5. Test connection:
   ```bash
   ssh -T git@github.com
   ```

✅ Now you can **clone, push, and pull** repositories securely:
```bash
git clone git@github.com:your-username/your-repo.git
```


## ✅ Final Check

- Python 3.11.7 is installed and available.  
- Virtual environment working correctly.  
- VS Code configured with Python interpreter.  
- Common dev tools installed (black, flake8, pytest).  
- Ready to start Python project development! 🎉  

---

## 📦 Recommended Packages for Modern Python Development

Below are some useful packages you may want to install depending on your project needs:

```bash
pip install fastapi uvicorn[standard] sqlalchemy aiosqlite httpx pydantic python-dotenv requests python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
```

### Package Overview
- **FastAPI** → High-performance web framework for building APIs with Python.  
- **Uvicorn[standard]** → ASGI server (with extras like `uvloop` and `httptools`) for running FastAPI or other async web apps.  
- **SQLAlchemy** → Powerful ORM (Object Relational Mapper) for database interaction.  
- **aiosqlite** → Async support for SQLite database access.  
- **httpx** → Modern async HTTP client for making API requests.  
- **Pydantic** → Data validation and settings management using Python type hints.  
- **python-dotenv** → Loads environment variables from `.env` files for configuration.  
- **Requests** → Popular HTTP library for synchronous API calls.  
- **python-jose[cryptography]==3.3.0** → JWT (JSON Web Token) implementation for authentication & authorization.  
- **passlib[bcrypt]==1.7.4** → Password hashing library with bcrypt support.  

---

✅ With these packages, you can build production-ready APIs, handle databases, secure authentication, manage async/sync requests, and keep configuration clean.

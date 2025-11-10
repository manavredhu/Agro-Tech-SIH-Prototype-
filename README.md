
# Agro-Tech-SIH-Prototype-

Agro-Tech (AgroTech) is a small prototype demonstrating an AI-enabled farming assistant. It contains a FastAPI backend that serves agricultural data and simple routes for soil, weather and irrigation, plus a minimal frontend (static HTML/JS/CSS) that can be used for demos.

This README explains how to set up and run the project locally and with Docker, where to find the main components, and a few maintenance tips.

## Contents

- `Agrobot/Agrobot ai final backend/` — FastAPI backend, `Dockerfile`, `docker-compose.yml`, and scripts like `seed.py` and `smoketest.sh`.
- `Agrobot/Agrobot ai final frontend/` — static demo frontend (`index.html`, `script.js`, `style.css`).

## Quick start (recommended)

Prerequisites:
- Git
- Python 3.8+
- pip
- (optional) Docker & docker-compose

Run backend locally (virtualenv recommended):

1. Open a terminal in the backend folder:

```powershell
Set-Location -Path "c:\Users\manav\OneDrive\Desktop\AGRO_bot.ai-Prototype-main\Agrobot\Agrobot ai final backend"
```

2. Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the FastAPI server (example):

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` and (if used) the automatic docs at `http://localhost:8000/docs`.

Run frontend:
- The frontend is static. Open `Agrobot/Agrobot ai final frontend/index.html` in a browser. For local API integration, update the frontend API base URL in `script.js` if needed.

## Docker (one-line)

From the backend root you can build and run with Docker Compose:

```powershell
Set-Location -Path "c:\Users\manav\OneDrive\Desktop\AGRO_bot.ai-Prototype-main\Agrobot\Agrobot ai final backend"
docker-compose up --build
```

## Seed data and tests

- `seed.py` is provided to populate sample data — run it against the configured database after starting the backend.
- `smoketest.sh` contains simple checks; on Windows run equivalent PowerShell commands or use WSL.

## Project structure (high level)

- `app/` — Python package for the backend.
	- `main.py` — FastAPI app entrypoint.
	- `routers/` — endpoints grouped by domain: `soil.py`, `weather.py`, `irrigation.py`, `faostat.py`, `auth.py`.
	- `models.py`, `db.py`, `config.py` — data and configuration.

## Recommended cleanup (optional but suggested)

The repository currently contains some OS/editor artifacts (e.g., `.DS_Store`, `__pycache__`, compiled files). A `.gitignore` was added, but these files are already tracked in history. If you want me to remove them from the repository (safe: remove from latest commit; or destructive: purge from history), tell me which option you prefer and I will proceed.

## Line endings

When working on Windows Git may warn about LF/CRLF conversions. To standardize, consider adding a `.gitattributes` to enforce e.g. `* text=auto` or a policy that fits your team.

## Contributing

If you want help improving this project I can:

- Remove tracked junk files and push a cleanup commit.
- Add a small CI workflow (GitHub Actions) for linting/tests.
- Add a `Makefile`/`PowerShell` helper script to run common tasks.

## License

See the repository `LICENSE` file (if present).

## Contact

If you want more polish (detailed setup, example env vars, or a deploy guide) tell me what platform you plan to deploy to (e.g., Heroku, DigitalOcean, Azure) and I will add targeted instructions.


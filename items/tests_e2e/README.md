E2E tests (Playwright)

Requirements (local):
- Python 3.8+
- Install Playwright and pytest: `pip install playwright pytest pytest-playwright`
- Install browsers: `python -m playwright install`

Run the single test:
- Ensure your dev server is running (e.g., `python manage.py runserver`).
- From the repo root: `pytest items/tests_e2e/test_loader_back.py -q`

Artifacts:
- On failure the test will write artifacts under `test-artifacts/playwright/` (trace.zip, video files, and screenshots when applicable).
- The CI workflow will upload any files in `test-artifacts/**` when the job fails.

Quick setup (local):
- Run the provided setup script to install dependencies and browsers:
  - macOS / Linux: `./scripts/setup_e2e.sh`
  - Windows (PowerShell/CMD): `scripts\setup_e2e.bat`
- Then start the server: `python manage.py runserver`
- Run the test: `pytest items/tests_e2e/test_loader_back.py -q`

Notes:
- The test assumes the app runs at http://localhost:8000/.
- CI: add a job that installs Python deps and runs `python -m playwright install` before `pytest`. Make sure the workflow uploads `test-artifacts/` on failure (this repo includes such a workflow).

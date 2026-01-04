@echo off
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install --with-deps
echo Playwright setup complete. Run: pytest items/tests_e2e/test_loader_back.py -q

import os
import pytest
try:
    from playwright.sync_api import sync_playwright
except Exception as e:
    raise RuntimeError(
        "Playwright is not installed or not importable.\n"
        "Install dependencies: 'python -m pip install playwright pytest-playwright'\n"
        "Then install browsers: 'python -m playwright install --with-deps'\n"
        "Run tests with the same interpreter: 'python -m pytest items/tests_e2e'\n"
        "Original error: {}".format(e)
    )

ARTIFACT_DIR = os.path.join("test-artifacts", "playwright")


def pytest_runtest_makereport(item, call):
    # Set the test outcome on the item so fixtures can inspect it
    if call.when == 'call':
        setattr(item, "rep_call", call)


@pytest.fixture(scope='function')
def pw_page(request):
    """Provide a Playwright page with video recording and tracing enabled.

    Traces, videos and screenshots are saved to `test-artifacts/playwright/`.
    On test failure a screenshot will be saved and tracing will be stopped and written.
    """
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(record_video_dir=ARTIFACT_DIR)
    # start tracing for this context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page

    # Teardown: check test result and save artifacts
    rep = getattr(request.node, "rep_call", None)
    try:
        if rep and rep.failed:
            # Save screenshot
            try:
                screenshot_path = os.path.join(ARTIFACT_DIR, f"{request.node.name}-failure-screenshot.png")
                page.screenshot(path=screenshot_path, full_page=True)
            except Exception:
                pass

        # Stop tracing and save trace file
        try:
            trace_path = os.path.join(ARTIFACT_DIR, f"{request.node.name}-trace.zip")
            context.tracing.stop(path=trace_path)
        except Exception:
            pass

        # Close context (will flush video)
        try:
            context.close()
        except Exception:
            pass

        try:
            browser.close()
        except Exception:
            pass

    finally:
        try:
            pw.stop()
        except Exception:
            pass
import pytest

BASE_URL = "http://localhost:8000/"

@pytest.mark.skipif(False, reason="Run only when Playwright is installed and server is running")
def test_loader_hidden_on_back(pw_page):
    """Clicks the report button, waits for the overlay, goes back and ensures the overlay is hidden and the button is restored.

    Uses the `pw_page` fixture which records video and tracing. Artifacts are saved to `test-artifacts/playwright/`.
    """
    page = pw_page

    page.goto(BASE_URL)

    # Wait for the report button
    page.wait_for_selector("a.btn-report", timeout=5000)

    # Click the report button
    page.click("a.btn-report")

    # Ensure the loader becomes visible
    page.wait_for_selector("#page-loader", state="visible", timeout=5000)

    # Navigate back (simulate browser Back action)
    page.go_back()

    # Wait for loader to be hidden again
    page.wait_for_selector("#page-loader", state="hidden", timeout=5000)

    # The report button should not have buffering class
    assert page.query_selector("a.btn-report.is-buffering") is None

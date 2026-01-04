import os
import pytest

BASE_URL = "http://localhost:8000/"
ARTIFACT_DIR = os.path.join("test-artifacts", "playwright")

@pytest.mark.skipif(False, reason="Run only when Playwright is installed and server is running")
def test_upload_and_view_detail(pw_page):
    page = pw_page

    # Prepare an image file to upload
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    img_path = os.path.join(ARTIFACT_DIR, 'upload-test.png')
    with open(img_path, 'wb') as f:
        # Minimal 1x1 PNG
        f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82")

    # Go to upload page
    page.goto(BASE_URL + 'upload/')

    page.wait_for_selector('input[name="name"]')
    page.fill('input[name="name"]', 'E2E Test Item')
    page.fill('input[name="finder_name"]', 'E2E Tester')
    page.fill('input[name="finder_contact"]', '1234567890')
    # Select category 'Other' (works if option exists)
    page.select_option('select[name="category"]', 'Other')
    page.fill('textarea[name="description"]', 'Uploaded by E2E test')

    # Set lat/lng hidden inputs directly
    page.evaluate("() => { document.getElementById('lat').value='12.345678'; document.getElementById('lng').value='98.765432'; }")

    # Upload file
    page.set_input_files('input[type="file"]', img_path)

    # Submit form
    page.click('button[type="submit"]')

    # After submitting, should redirect to list and show the new item
    page.wait_for_selector("text=E2E Test Item", timeout=5000)

    # Click the item's card overlay to view details
    card = page.locator('div.card', has_text='E2E Test Item').first
    card.locator('a.card-overlay').click()

    # Verify detail page content
    page.wait_for_selector('text=E2E Test Item', timeout=5000)
    assert page.query_selector('text=Uploaded by E2E test') is not None
    assert page.query_selector('text=VIEW ON MAP') is not None
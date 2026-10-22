from pathlib import Path
from playwright.sync_api import sync_playwright


root = Path(__file__).resolve().parents[2]
html = root / "forward" / "web-fixture" / "index.html"
output = root.parent / "test-results" / "web-fixture.png"
output.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 900, "height": 720})
    page.goto(html.as_uri())
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Save and continue").click()
    assert page.locator("#save-result").inner_text() == ""
    page.screenshot(path=str(output), full_page=True)
    browser.close()

print(output)

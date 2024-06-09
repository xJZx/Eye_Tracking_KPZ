from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import io


def get_full_page_screenshot(driver, url):
    # Open the website
    driver.get(url)

    # Allow some time for the page to load
    time.sleep(3)

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Set up the PIL image to stitch screenshots
    stitched_image = Image.new('RGB', (driver.execute_script("return document.body.scrollWidth"), total_height))

    current_scroll_position = 0
    while current_scroll_position < total_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(2)  # Adjust time as needed for page to render

        screenshot = driver.get_screenshot_as_png()
        screenshot_image = Image.open(io.BytesIO(screenshot))

        # Calculate the position to paste the screenshot
        paste_position = (0, current_scroll_position)
        stitched_image.paste(screenshot_image, paste_position)

        current_scroll_position += viewport_height

    return stitched_image


# Set up the WebDriver (here using Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # URL of the website
    url = 'https://comarch.pl'  # Replace with the website you want to open

    # Get the full page screenshot
    full_page_screenshot = get_full_page_screenshot(driver, url)

    # Optionally, save the full page screenshot to a file
    full_page_screenshot.save('full_page_screenshot.png')
    print("Screenshot saved as 'full_page_screenshot.png'")

finally:
    # Close the browser
    driver.quit()

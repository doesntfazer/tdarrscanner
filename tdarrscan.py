from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

# Fetch URLs from environment variables or default to the given ones if not found
SONARR_URL = os.environ.get('SONARR_URL', 'http://192.168.0.33:8265/#/libraries/l6pK7YCUy/source')
RADARR_URL = os.environ.get('RADARR_URL', 'http://192.168.0.33:8265/#/libraries/0WEwzc7OF/source')

@app.route('/', methods=['POST'])
def catch_all():
    payload = request.json

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/opt/google/chrome/google-chrome"

    driver = webdriver.Chrome(options=chrome_options)

    if 'series' in payload:
        driver.get(SONARR_URL)
    elif 'movie' in payload:
        driver.get(RADARR_URL)
    else:
        print(f"Unknown payload type: {payload}")
        driver.quit()
        return "Payload not recognized", 400

    try:
        # Assuming the dropdown button must be clicked to reveal the actual button.
        dropdown = driver.find_element(By.ID, "dropdown-basic")
        dropdown.click()

        # Then click the actual button
        button = driver.find_element(By.ID, "scanFindNew")
        button.click()

        # Wait for a few seconds to ensure scan happens
        driver.implicitly_wait(3)
    except Exception as e:
        print(f"Error interacting with page: {e}")
    finally:
        driver.quit()

    return "Done", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


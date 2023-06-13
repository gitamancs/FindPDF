import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options (optional)
chrome_options = webdriver.ChromeOptions()
# Add any desired options, e.g., headless mode, user agent, etc.
chrome_options.add_argument('--headless')

# Create an instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Anti-Captcha API key
api_key = 'a95c9d68c30dc4e57ba51e35e562afa8'

# Anti-Captcha API endpoint
api_url = 'https://api.anti-captcha.com/solve'

# Function to solve the captcha using Anti-Captcha service
def solve_captcha(image_url):
    # Request payload
    payload = {
        'clientKey': api_key,
        'task': {
            'type': 'ImageToTextTask',
            'body': image_url
        }
    }

    # Make the API request
    response = requests.post(api_url, json=payload)

    # Process the API response
    if response.status_code == 200:
        captcha_solution = response.json().get('solution').get('text')
        return captcha_solution
    else:
        print('Error solving captcha:', response.text)
        return ""  # Return an empty string if captcha solution is not available


# Navigate to the website
driver.get('https://ceoelection.maharashtra.gov.in/searchlist/')

# Function to automate the process
def automate_download(select_district):
    # Select the District
    district_select = driver.find_element(By.ID, 'ctl00_Content_DistrictList')
    district_select.send_keys(select_district)

    # Wait for the page to load
    time.sleep(2)

    # Get the Assembly Constituencies
    ac_select = driver.find_element(By.ID, 'ctl00_Content_AssemblyList')
    ac_options = ac_select.find_elements(By.TAG_NAME, 'option')

    # Loop through the Assembly Constituencies
    for ac_option in ac_options[1:]:
        # Select the Assembly Constituency
        ac_option.click()

        # Wait for the page to load
        time.sleep(2)

        # Get the Parts
        part_select = driver.find_element(By.ID, 'ctl00_Content_PartList')
        part_options = part_select.find_elements(By.TAG_NAME, 'option')

        # Loop through the Parts
        for part_option in part_options[1:]:
            # Select the Part
            part_option.click()

            # Wait for the page to load
            time.sleep(2)

            # Solve the captcha automatically
            captcha_field = driver.find_element(By.ID, 'ctl00_Content_txtcaptcha')

            captcha_image = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'img')))
            captcha_image_url = captcha_image.get_attribute('src')
            captcha_solution = solve_captcha(captcha_image_url)

            # Check if captcha_solution is not None before sending keys
            if captcha_solution is not None:
                # Enter the captcha solution
                captcha_field.clear()
                captcha_field.send_keys(captcha_solution)

                # Click on 'Open PDF' to download the voter list
                open_pdf_button = driver.find_element(By.ID, 'ctl00_Content_OpenButton')
                open_pdf_button.click()

                # Wait for the file to download
                time.sleep(5)  # Adjust the time if necessary
            else:
                print('Error: Failed to solve captcha')

            # Enter the captcha solution
            captcha_field.clear()
            captcha_field.send_keys(captcha_solution)

            # Click on 'Open PDF' to download the voter list
            open_pdf_button = driver.find_element(By.ID, 'ctl00_Content_OpenButton')
            open_pdf_button.click()

            # Wait for the file to download
            time.sleep(5)  # Adjust the time if necessary

# Call the automation function with the desired district
automate_download('Pune')

# Close the browser
driver.quit()

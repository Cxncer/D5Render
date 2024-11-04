import json
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 1. Generate a temporary email using Temp-Mail API
def create_temp_email():
    temp_mail_url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
    response = requests.get(temp_mail_url)
    email = response.json()[0]
    return email

# 2. Set up account creation details
def generate_random_password(length=10):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

# 3. Automate the account creation process
def create_account(email, password):
    # Set up Chrome options for headless execution
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Specify the path to the Chrome binary
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update this to your actual Chrome executable path

    # Specify the correct path to your ChromeDriver
    service = Service(executable_path="./chromedriver")  # Ensure 'chromedriver' is in the workspace directory
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://myspace.d5render.com/login")
    
    # Rest of your account creation logic...

    return driver

# 4. Retrieve email verification code from Temp-Mail
def get_verification_code(email):
    username, domain = email.split('@')
    temp_mail_check_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    time.sleep(10)  # Wait for email to arrive
    
    response = requests.get(temp_mail_check_url).json()
    email_id = response[0]['id']
    
    # Get email content
    email_content_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={email_id}"
    email_content = requests.get(email_content_url).json()
    verification_code = email_content['textBody']  # Adjust parsing based on actual email content
    
    return verification_code

# 5. Verify email
def enter_verification_code(driver, code):
    verification_field = driver.find_element(By.NAME, "verification_code")
    verification_field.send_keys(code)
    driver.find_element(By.ID, "verifyButton").click()  # Assuming there's a "Verify" button

# 6. Save the login details
def save_credentials(email, password):
    credentials = {
        "email": email,
        "password": password
    }
    with open("account_details.json", "w") as f:
        json.dump(credentials, f)

# Main workflow
email = create_temp_email()
password = generate_random_password()
driver = create_account(email, password)

# After registration, retrieve the code and verify
verification_code = get_verification_code(email)
enter_verification_code(driver, verification_code)

# Save login credentials
save_credentials(email, password)
driver.quit()

print(f"Account created successfully with email: {email} and password: {password}")

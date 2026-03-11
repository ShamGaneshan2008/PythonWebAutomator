from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

load_dotenv()


class WebAutomation:

    def __init__(self):
        self.driver = None

    def _log(self, message, level="info"):
        print(f"[{level.upper()}] {message}")

    # -----------------------------
    # Start Browser
    # -----------------------------
    def start_browser(self):
        try:
            self._log("Starting Chrome browser")

            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")

            download_path = os.getcwd()
            prefs = {"download.default_directory": download_path}
            chrome_options.add_experimental_option("prefs", prefs)

            service = Service(ChromeDriverManager().install())

            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self._log("Browser started successfully")

        except WebDriverException as e:
            print(f"[ERROR] Browser failed: {e}")

    # -----------------------------
    # Login
    # -----------------------------
    def login(self, username: str, password: str):
        """Navigate to demoqa.com/login and log in."""

        if not self.driver:
            self.start_browser()

        self._log("Navigating to login page…")

        self.driver.get("https://demoqa.com/login")

        wait = WebDriverWait(self.driver, 10)

        username_field = wait.until(
            EC.visibility_of_element_located((By.ID, "userName"))
        )

        password_field = wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )

        login_button = self.driver.find_element(By.ID, "login")

        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)

        self.driver.execute_script("arguments[0].click();", login_button)

        self._log("Login submitted")

    # -----------------------------
    # Fill Form
    # -----------------------------
    def fill_form(self, fullname, email, current_address, permanent_address):

        try:
            wait = WebDriverWait(self.driver, 10)

            self._log("Opening Text Box form...")

            elements_group = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/div/div[1]/span/div')
                )
            )

            elements_group.click()

            text_box = wait.until(
                EC.element_to_be_clickable((By.ID, "item-0"))
            )

            text_box.click()

            wait.until(EC.visibility_of_element_located((By.ID, "userName"))).send_keys(fullname)
            wait.until(EC.visibility_of_element_located((By.ID, "userEmail"))).send_keys(email)
            wait.until(EC.visibility_of_element_located((By.ID, "currentAddress"))).send_keys(current_address)
            wait.until(EC.visibility_of_element_located((By.ID, "permanentAddress"))).send_keys(permanent_address)

            submit = self.driver.find_element(By.ID, "submit")
            submit.click()

            self._log("Form submitted successfully", "success")

        except Exception as e:
            print(f"[ERROR] Form error: {e}")

    # -----------------------------
    # Download File
    # -----------------------------
    def download(self):

        try:
            wait = WebDriverWait(self.driver, 10)

            upload_download = wait.until(
                EC.element_to_be_clickable((By.ID, "item-7"))
            )

            upload_download.click()

            download_button = wait.until(
                EC.element_to_be_clickable((By.ID, "downloadButton"))
            )

            download_button.click()

            self._log("Download started")

        except Exception as e:
            print(f"[ERROR] Download error: {e}")

    # -----------------------------
    # Close Browser
    # -----------------------------
    def close(self):

        if self.driver:
            self.driver.quit()
            self._log("Browser closed")


# -----------------------------
# Run Script
# -----------------------------
if __name__ == "__main__":

    bot = WebAutomation()

    bot.start_browser()

    bot.login("username", "password")

    bot.fill_form()

    bot.download()

    bot.close()
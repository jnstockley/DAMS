import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        OPTIONS.add_argument("--no-sandbox")
        OPTIONS.add_argument("--disable-dev-shm-usage")
        self.DRIVER = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=OPTIONS
        )
        self.ROOT_URL = "http://127.0.0.1:5000"

    def test_login(self):
        self.DRIVER.get(f"{self.ROOT_URL}/login")
        self.assertEqual("Login", self.DRIVER.find_element(By.CLASS_NAME, "title").text)
        self.assertTrue(self.DRIVER.find_element(By.NAME, "email"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "password"))
        LOGIN_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "button")
        self.assertTrue(LOGIN_BUTTON)
        self.assertEqual(LOGIN_BUTTON.tag_name, "button")

    def test_login_post(self):
        self.DRIVER.get(f"{self.ROOT_URL}/login")

        LOGIN_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "button")
        LOGIN_BUTTON.click()
        self.assertTrue(self.DRIVER.find_element(By.CLASS_NAME, "is-danger"))
        self.assertEquals(self.DRIVER.current_url, f"{self.ROOT_URL}/login")
        EMAIL = self.DRIVER.find_element(By.NAME, "email")
        EMAIL.send_keys("vinaypursnani@icloud.com")
        PASSWORD = self.DRIVER.find_element(By.NAME, "password")
        PASSWORD.send_keys("Qwerty12345")
        LOGIN_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "button")
        LOGIN_BUTTON.click()
        self.assertTrue(self.DRIVER.current_url, f"{self.ROOT_URL}/donor")

    def tearDown(self):
        self.DRIVER.close()

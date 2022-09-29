import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        self.DRIVER: webdriver = webdriver.Chrome('../chromedriver', options=OPTIONS)
        self.ROOT_URL = "http://127.0.0.1:5000"

    def test_register(self):
        self.DRIVER.get(f'{self.ROOT_URL}/register')
        self.assertEqual("Sign Up", self.DRIVER.find_element(By.CLASS_NAME, "title").text)
        self.assertTrue(self.DRIVER.find_element(By.NAME, "first-name"))
        SIGN_UP_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "sign-up")
        self.assertTrue(SIGN_UP_BUTTON)
        self.assertEqual(SIGN_UP_BUTTON.tag_name, "button")

    def test_register_post(self):
        self.DRIVER.get(f'{self.ROOT_URL}/register')
        LAST_NAME = self.DRIVER.find_element(By.NAME, "last-name")
        STREET_ADDRESS = self.DRIVER.find_element(By.NAME, "street-address")
        CITY = self.DRIVER.find_element(By.NAME, "city")
        STATE = self.DRIVER.find_element(By.NAME, "state")
        ZIP_CODE = self.DRIVER.find_element(By.NAME, "zip-code")
        COUNTRY = self.DRIVER.find_element(By.NAME, "country")
        EMAIL = self.DRIVER.find_element(By.NAME, "email")
        PASSWORD = self.DRIVER.find_element(By.NAME, "password")
        CONFIRM_PASSWORD = self.DRIVER.find_element(By.NAME, "confirm-password")
        ACCOUNT_TYPE = self.DRIVER.find_element(By.NAME, "account-type")
        SIGN_UP_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "sign-up")
        SIGN_UP_BUTTON.click()
        self.assertTrue(self.DRIVER.find_element(By.CLASS_NAME, "is-danger"))
        self.assertEquals(self.DRIVER.current_url, f'{self.ROOT_URL}/register')
        FIRST_NAME = self.DRIVER.find_element(By.NAME, "first-name")
        FIRST_NAME.send_keys("1234")
        # self.assertTrue(self.DRIVER.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div/div").text == "1234 is not a valid First Name!")
        print(f'Text: {self.DRIVER.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div/div").text}')
        # time.sleep(5)

    def test_verify_account(self):
        self.DRIVER.get(f'{self.ROOT_URL}/verify-account')
        self.assertEqual("Verify Account", self.DRIVER.find_element(By.CLASS_NAME, "title").text)
        self.assertTrue(self.DRIVER.find_element(By.NAME, "email"))
        VERIFY_ACCOUNT_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "verify-account")
        self.assertTrue(VERIFY_ACCOUNT_BUTTON)
        self.assertEqual(VERIFY_ACCOUNT_BUTTON.tag_name, "button")

    def test_verify_account_post(self):
        self.skipTest("Not Implemented")

    def tearDown(self):
        self.DRIVER.close()

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        self.DRIVER: webdriver = webdriver.Chrome('../../chromedriver', options=OPTIONS)
        self.ROOT_URL = "http://127.0.0.1:5000"

    def test_register(self):
        self.DRIVER.get(f'{self.ROOT_URL}/register')
        self.assertEqual("Sign Up", self.DRIVER.find_element(By.CLASS_NAME, "title").text)
        self.assertTrue(self.DRIVER.find_element(By.NAME, "first-name"))
        SIGN_UP_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "sign-up")
        self.assertTrue(SIGN_UP_BUTTON)
        self.assertEqual(SIGN_UP_BUTTON.tag_name, "button")

    def test_register_post(self):
        self.skipTest("Not Implemented")

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

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class RegisterTestCase(unittest.TestCase):

    ERROR_MESSAGE = "notification"

    # URI
    REGISTER_URI = "/register"
    VERIFY_ACCOUNT_URI = "/verify-account"

    # Elements on Registration Page
    REGISTER_TITLE = "Sign Up"
    REGISTER_TITLE_ELM = "sign-up-title"
    FIRST_NAME = "first-name"
    LAST_NAME = "last-name"
    STREET_ADDRESS = "street-address"
    CITY = "city"
    STATE = "state"
    ZIP_CODE = "zip-code"
    COUNTRY = "country"
    EMAIL = "email"
    PASSWORD = "password"
    CONFIRM_PASSWORD = "confirm-password"
    ACCOUNT_TYPE = "account-type"
    SIGN_UP_BTN = "sign-up"

    # Elements on Verify Account Page
    VERIFICATION_TITLE = "Verify Account"
    VERIFICATION_TITLE_ELM = "verify-account-title"
    VERIFY_EMAIL = "verify-email"
    SECURITY_CODE = "security-code"
    VERIFY_ACCOUNT_BTN = "verify-account"

    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        OPTIONS.add_argument("--no-sandbox")
        OPTIONS.add_argument("--disable-dev-shm-usage")
        self.DRIVER = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=OPTIONS
        )
        self.ROOT_URL = "http://127.0.0.1:5000"

    def test_register(self):
        self.DRIVER.get(f"{self.ROOT_URL}{self.REGISTER_URI}")

        # Sign Up Text
        self.assertTrue(
            self.DRIVER.find_element(By.CLASS_NAME, self.REGISTER_TITLE_ELM)
        )
        self.assertEqual(
            self.REGISTER_TITLE,
            self.DRIVER.find_element(By.CLASS_NAME, self.REGISTER_TITLE_ELM).text,
        )
        self.assertEqual(
            self.DRIVER.find_element(By.CLASS_NAME, self.REGISTER_TITLE_ELM).tag_name,
            "h3",
        )

        # First Name Text Input
        self.assertTrue(self.DRIVER.find_element(By.NAME, self.FIRST_NAME))
        self.assertEqual(
            self.DRIVER.find_element(By.NAME, self.FIRST_NAME).tag_name, "input"
        )

        # Account Type Dropdown
        self.assertTrue(self.DRIVER.find_element(By.NAME, self.ACCOUNT_TYPE))
        self.assertEqual(
            self.DRIVER.find_element(By.NAME, self.ACCOUNT_TYPE).tag_name, "select"
        )

        # Sign Up Button
        self.assertTrue(self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN))
        self.assertEqual(
            self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).tag_name, "button"
        )

    def test_register_post(self):
        # self.skipTest("Not Implemented")
        self.DRIVER.get(f"{self.ROOT_URL}{self.REGISTER_URI}")

        # Short First Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("ja")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(self.checkErrorMessage("ja is not a valid First Name!"))

        # Numbers in First Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack2")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(self.checkErrorMessage("jack2 is not a valid First Name!"))

        # Spaces in First Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack s")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(self.checkErrorMessage("jack s is not a valid First Name!"))

        # Short Last Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack")
        self.DRIVER.find_element(By.NAME, self.LAST_NAME).send_keys("ja")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(self.checkErrorMessage("ja is not a valid Last Name!"))

        # Numbers in Last Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack")
        self.DRIVER.find_element(By.NAME, self.LAST_NAME).send_keys("jack2")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(self.checkErrorMessage("jack2 is not a valid Last Name!"))

        # Spaces in Last Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack")
        self.DRIVER.find_element(By.NAME, self.LAST_NAME).send_keys("jack s")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(self.checkErrorMessage("jack s is not a valid Last Name!"))

        # Missing House Number
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack")
        self.DRIVER.find_element(By.NAME, self.LAST_NAME).send_keys("stockley")
        self.DRIVER.find_element(By.NAME, self.STREET_ADDRESS).send_keys(
            "Meadowland Circle"
        )
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(
            self.checkErrorMessage("Meadowland Circle is not a valid Street Address!")
        )

        # Missing Street Name
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack")
        self.DRIVER.find_element(By.NAME, self.LAST_NAME).send_keys("stockley")
        self.DRIVER.find_element(By.NAME, self.STREET_ADDRESS).send_keys("25831 Circle")
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(
            self.checkErrorMessage("25831 Circle is not a valid Street Address!")
        )

        # Missing Street Abbreviation
        self.DRIVER.find_element(By.NAME, self.FIRST_NAME).send_keys("jack")
        self.DRIVER.find_element(By.NAME, self.LAST_NAME).send_keys("stockley")
        self.DRIVER.find_element(By.NAME, self.STREET_ADDRESS).send_keys(
            "25831 Meadowland"
        )
        self.DRIVER.find_element(By.NAME, self.SIGN_UP_BTN).click()
        self.assertTrue(
            self.checkErrorMessage("25831 Meadowland is not a valid Street Address!")
        )

    def test_verify_account(self):
        self.DRIVER.get(f"{self.ROOT_URL}{self.VERIFY_ACCOUNT_URI}")

        # Verification Text
        self.assertTrue(
            self.DRIVER.find_element(By.CLASS_NAME, self.VERIFICATION_TITLE_ELM)
        )
        self.assertEqual(
            self.VERIFICATION_TITLE,
            self.DRIVER.find_element(By.CLASS_NAME, self.VERIFICATION_TITLE_ELM).text,
        )
        self.assertEqual(
            self.DRIVER.find_element(
                By.CLASS_NAME, self.VERIFICATION_TITLE_ELM
            ).tag_name,
            "h3",
        )

        # Verify Email Text Input
        self.assertTrue(self.DRIVER.find_element(By.NAME, self.VERIFY_EMAIL))
        self.assertEqual(
            self.DRIVER.find_element(By.NAME, self.VERIFY_EMAIL).tag_name, "input"
        )

        # Security Code Input
        self.assertTrue(self.DRIVER.find_element(By.NAME, self.SECURITY_CODE))
        self.assertEqual(
            self.DRIVER.find_element(By.NAME, self.SECURITY_CODE).tag_name, "input"
        )

        # Verify Account Button
        self.assertTrue(self.DRIVER.find_element(By.NAME, self.VERIFY_ACCOUNT_BTN))
        self.assertEqual(
            self.DRIVER.find_element(By.NAME, self.VERIFY_ACCOUNT_BTN).tag_name,
            "button",
        )

    def test_verify_account_post(self):
        self.skipTest("Not Implemented")

    def tearDown(self):
        self.DRIVER.close()

    def checkErrorMessage(self, message):
        return (
            self.DRIVER.find_element(By.CLASS_NAME, self.ERROR_MESSAGE).text == message
        )

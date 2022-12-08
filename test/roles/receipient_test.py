import unittest
from random import randrange

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


class RecipientTestCase(unittest.TestCase):
    RECIPIENT_URI = "/request"

    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        OPTIONS.add_argument("--no-sandbox")
        OPTIONS.add_argument("--disable-dev-shm-usage")
        self.DRIVER = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=OPTIONS
        )
        self.ROOT_URL = "http://127.0.0.1:5000"

    def recipient_login(self):
        self.DRIVER.get(f"{self.ROOT_URL}")
        EMAIL = self.DRIVER.find_element(By.NAME, "email")
        EMAIL.send_keys("jnstockley@uiowa.edu")
        PASSWORD = self.DRIVER.find_element(By.NAME, "password")
        PASSWORD.send_keys("Password123")
        LOGIN_BUTTON = self.DRIVER.find_element(By.CLASS_NAME, "button")
        LOGIN_BUTTON.click()
        return self.DRIVER.current_url == f"{self.ROOT_URL}{self.RECIPIENT_URI}"

    def test_recipient(self):
        self.assertTrue(self.recipient_login())
        self.assertTrue(self.DRIVER.find_element(By.NAME, "event"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "item"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "quantity"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "link"))

    def test_recipient_post(self):
        self.assertTrue(self.recipient_login())
        EVENTS = self.DRIVER.find_element(By.NAME, "event")
        ITEMS = self.DRIVER.find_element(By.NAME, "item")
        QUANTITY = self.DRIVER.find_element(By.NAME, "quantity")
        LINK_BUTTON = self.DRIVER.find_element(By.NAME, "link")
        EVENT_SIZE = len(Select(EVENTS).options)
        ITEMS_SIZE = len(Select(ITEMS).options)
        Select(EVENTS).select_by_index(randrange(0, EVENT_SIZE))
        Select(ITEMS).select_by_index(randrange(0, ITEMS_SIZE))
        QUANTITY.send_keys(randrange(1, 15))
        LINK_BUTTON.click()
        self.assertEqual(
            self.DRIVER.current_url, f"{self.ROOT_URL}{self.RECIPIENT_URI}"
        )
        self.assertTrue(self.DRIVER.find_element(By.NAME, "event"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "item"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "quantity"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "link"))

    def tearDown(self):
        self.DRIVER.close()

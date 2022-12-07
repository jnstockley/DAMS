import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class DonorTestCase(unittest.TestCase):

    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        OPTIONS.add_argument("--no-sandbox")
        OPTIONS.add_argument("--disable-dev-shm-usage")
        self.DRIVER = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=OPTIONS)
        self.ROOT_URL = "http://127.0.0.1:5000"

    def donor(self):
        return

    def donor_post(self):
        return

    def tearDown(self):
        self.DRIVER.close()

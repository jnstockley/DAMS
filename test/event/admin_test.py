import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService



class AdminTestCase(unittest.TestCase):

    def setUp(self):
        OPTIONS = Options()
        OPTIONS.headless = True
        OPTIONS.add_argument("--no-sandbox")
        OPTIONS.add_argument("--disable-dev-shm-usage")
        self.DRIVER = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=OPTIONS)
        self.ROOT_URL = "http://127.0.0.1:5000"



    def test_createEvent_post(self):
        self.DRIVER.get(f'{self.ROOT_URL}/create-event')
        #self.assertEqual("Create Event", self.DRIVER.find_element(By.CLASS_NAME, "title").text)
        self.assertTrue(self.DRIVER.find_element(By.NAME, "event-name"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "town-name"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "state-name"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "country-name"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "zipcodeNum"))
        self.assertTrue(self.DRIVER.find_element(By.NAME, "severity-level"))

        create_event_button = self.DRIVER.find_element(By.CLASS_NAME, "create-event")
        self.assertTrue(create_event_button)
        self.assertEqual(create_event_button.tag_name, "button")

    def tearDown(self):
        self.DRIVER.close()
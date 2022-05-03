from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import unittest
import time


MAX_TIME = 5


class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):
        if STAGING_SERVER := os.environ.get('STAGING_SERVER'):
            self.live_server_url = 'http://' + STAGING_SERVER

        if os.environ.get('HEADLESS', False):
            options = Options()
            options.headless = True
            self.browser = webdriver.Chrome(options=options)
        else:
            self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_to_check_text_in_table(self, text):
        START_TIME = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')

                self.assertIn(
                    text,
                    [row.text for row in rows]
                )
                return 
            except (AssertionError, WebDriverException) as e:
                if time.time() - START_TIME > MAX_TIME:
                    raise e
                time.sleep(0.2)
        


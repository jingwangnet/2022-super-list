from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import unittest
import time


MAX_TIME = 5


class NewVisitorTest(StaticLiveServerTestCase):
    
    def setUp(self):
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
        

    def test_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do lists', self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do lists', header)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy bread')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_to_check_text_in_table('1: Buy bread')


        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Eatting bread for dinner')
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('2: Eatting bread for dinner')
        self.wait_to_check_text_in_table('1: Buy bread')

    def test_start_multiple_lists_on_diffrent_urls(self):
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy bread')
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table("1: Buy bread")
        
        EDITH_URL = self.browser.current_url
        self.assertRegex(EDITH_URL, '/lists/.+/')

        self.browser.quit()
        self.setUp()

        self.browser.get(self.live_server_url)
        html = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy bread', html)
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Go shopping')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_to_check_text_in_table("1: Go shopping")
        html = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy bread', html)

        JOHN_URL = self.browser.current_url
        self.assertRegex(JOHN_URL, '/lists/.+/')
        self.assertNotEqual(JOHN_URL, EDITH_URL)
        

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=30
        )

        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1: Buy milk')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=30
        )

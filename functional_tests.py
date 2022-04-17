from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import unittest
import time

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        if os.environ.get('HEADLESS', False):
            options = Options()
            options.headless = True
            self.browser = webdriver.Chrome(options=options)
        else:
            self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_text_in_table(self, text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        self.assertIn(
            text,
            [row.text for row in rows]
        )
        

    def test_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://127.0.0.1:8000')
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
        time.sleep(1)
        
        self.check_text_in_table('1: Buy bread')


        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Eatting bread for dinner')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_text_in_table('2: Eatting bread for dinner')
        self.check_text_in_table('1: Buy bread')



if __name__ == '__main__':
    unittest.main()

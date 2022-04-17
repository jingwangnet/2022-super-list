from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import unittest

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

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        self.assertIn(
            '1: Buy bread',
            [row.text for row in rows]
        )



if __name__ == '__main__':
    unittest.main()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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


if __name__ == '__main__':
    unittest.main()

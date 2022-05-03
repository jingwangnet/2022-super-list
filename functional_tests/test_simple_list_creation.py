from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

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
        


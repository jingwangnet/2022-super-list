from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_items(self):
        self.browser.get(self.live_server_url)
        
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))
        

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1: Buy milk')

        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use milk to make tea')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('2: Use milk to make tea')
        self.wait_to_check_text_in_table('1: Buy milk')

    def test_cannot_save_duplicate_items(self):
        self.browser.get(self.live_server_url)
        
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1: Buy milk')

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has_error').text,
            DUPLICATE_ITEM_ERROR
        ))


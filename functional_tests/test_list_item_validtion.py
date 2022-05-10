from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_items(self):
        self.browser.get(self.live_server_url)
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has_error'),
            "You can't have an empty list item"
        ))

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1: Buy milk')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has_error'),
            "You can't have an empty list item"
        ))
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use milk to make tea')
        inputbox.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('2: Use milk to make tea')
        self.wait_to_check_text_in_table('1: Buy milk')

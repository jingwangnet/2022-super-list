from django.conf import settings
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools.commands import create_session_on_server

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(email)
        else:
            session_key = create_pre_authenticated_session(email)


        self.browser.get(self.live_server_url + "/404/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('edith@example.com')

        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, 'My lists').click()

        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Reticulate splines')
        )
        self.browser.find_element(By.LINK_TEXT, 'Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'click cows')
        )
        self.borwser.find_element(By.LINK_TEXT, 'Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements(By.LINK_TEXT('My lists')),
            []
        ))





from django.core import mail   
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import os
import poplib
import time
from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL(os.environ.get('TEST_EMAIL_PROVIDE'))
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ.get('TEST_PASSWORD'))
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf-8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
                       

    def test_can_get_email_link_to_log_in(self):
        if self.staging_server:
            test_email = os.environ.get('TEST_EMAIL')
        else:
            test_email = 'edith@example.com'
            
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(test_email)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        body = self.wait_for_email(test_email, SUBJECT)
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http[s]?://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)
 
        self.wait_to_be_logged_in(email=test_email)
        
        self.browser.find_element(By.LINK_TEXT,'Log out').click()

        self.wait_to_be_logged_out(email=test_email)
                
        


        


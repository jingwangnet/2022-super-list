from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token
import accounts.views

class SendLoginEmailViewTest(TestCase):

    def post_email_to_send_login_email(self, follow=False):
        return self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=follow)

    def test_redirects_to_homepage(self):
        response = self.post_email_to_send_login_email()
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_send_mail_to_address_form_post(self, mock_send_mail):
        self.post_email_to_send_login_email()

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_creates_token_accociated_with_email(self):
        self.post_email_to_send_login_email()
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.post_email_to_send_login_email()

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_adds_success_message(self):
        response = self.post_email_to_send_login_email(follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, 'success')


class LoginViewTest(TestCase):

    def test_redirects_to_homepage(self):
        response = self.client.get('/accounts/login?=abcd123')

        self.assertRedirects(response, '/')

    @patch('accounts.views.auth')
    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )


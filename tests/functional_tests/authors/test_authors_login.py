import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        self.action_user_in_login_page(user.username, string_password)

        # Usuário vê a mensagem de login com sucesso e seu nome
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_auth_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:auth')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        self.action_user_in_login_page('', '')

        # vê a mensagem de erro na tela
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_User_not_valid(self):
        self.action_user_in_login_page("Invalid_user", "Invalid_password")

        # vê a mensagem de erro na tela
        self.assertIn(
            'invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

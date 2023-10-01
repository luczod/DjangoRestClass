from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    # Template method pattern
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )

    def action_user_in_login_page(self, text_username, text_password):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(text_username)
        password_field.send_keys(text_password)

        # Usuário envia o formulário
        form.submit()
        return

    # def sleep(self, qtd=10):
    #     time.sleep(qtd)

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecipeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    # Mixins class sem herença design partners
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

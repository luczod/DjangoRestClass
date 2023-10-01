from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
# from unittest import TestCase


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),

    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, placeholder)

    @parameterized.expand([
        ('username', (
            'Required. '
            '150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.')),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password2'),

    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)

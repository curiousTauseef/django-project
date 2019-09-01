from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = SubscriptionForm()

    def test_has_fields(self):
        fields = ['name', 'email', 'cpf', 'phone']
        self.assertSequenceEqual(fields, list(self.form.fields))
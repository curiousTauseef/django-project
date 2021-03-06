from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')


    def test_get(self):
        """Must return status code 200"""
        self.assertEqual(200, self.resp.status_code)


    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')


    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))
        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)


    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')


    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Raphael Lima', cpf='12345678909',
                    email='raphael.aolima8@gmail.com', phone='13-99135-8063')
        self.resp = self.client.post('/inscricao/', data)


    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)


    def test_send_subscribe_email(self):
        """Should send 1 email"""
        self.assertEqual(1, len(mail.outbox))


    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})


    def test_post(self):
        self.assertEqual(200, self.resp.status_code)


    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')


    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


    def test_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(
            name='Raphael Lima',
            cpf='12345678909',
            email='raphael.aolima8@gmail.com',
            phone='13-99135-8063'
        )
        resp = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(resp, 'Inscrição realizada com sucesso!')

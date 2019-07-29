from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionTest(TestCase):
  def setUp(self):
    self.resp = self.client.get('/inscricao/')
  def test_get(self):
    """Must return status code 200"""
    self.assertEqual(200, self.resp.status_code)
  
  def test_template(self):
    """Must use subscriptions/subscription_form.html"""
    self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
  
  def test_input(self):
    self.assertContains(self.resp, '<form')
    self.assertContains(self.resp, '<input', 6)
    self.assertContains(self.resp, 'type="text"', 3)
    self.assertContains(self.resp, 'type="email"')
    self.assertContains(self.resp, 'type="submit"')
  
  def test_csrf(self):
    self.assertContains(self.resp, 'csrfmiddlewaretoken')
    
  def test_has_form(self):
    form = self.resp.context['form']
    self.assertIsInstance(form, SubscriptionForm)
  
  def test_has_fields(self):
    form = self.resp.context['form']
    self.assertSequenceEqual(['name', 'email', 'cpf', 'phone'], list(form.fields))
    

class SubscriptionPostTest(TestCase):
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
  
  def test_subscription_email_subject(self):
    email = mail.outbox[0]
    expect = 'Confirmação de inscrição'
    self.assertEqual(expect, email.subject)
  
  def test_subscription_email_from(self):
    email = mail.outbox[0]
    expect = 'contato@eventex.com.br'
    self.assertEqual(expect, email.from_email)
    
  def test_subscription_email_to(self):
    email = mail.outbox[0]
    expect = ['contato@eventex.com.br', 'raphael.aolima8@gmail.com']
    
    self.assertListEqual(expect, email.to)
  
  def test_subscription_email_body(self):
    email = mail.outbox[0]
    
    self.assertIn('Raphael Lima', email.body)
    self.assertIn('12345678909', email.body)
    self.assertIn('raphael.aolima8@gmail.com', email.body)
    self.assertIn('13-99135-8063', email.body)
    

class SubscribeInvalidPost(TestCase):
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
      

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
      data = dict(name='Raphael Lima', cpf='12345678909',
            email='raphael.aolima8@gmail.com', phone='13-99135-8063')
      resp = self.client.post('/inscricao/', data, follow=True)
      self.assertContains(resp, 'Inscrição realizada com sucesso!')
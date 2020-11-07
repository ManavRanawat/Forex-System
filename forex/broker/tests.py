from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Broker


class BrokerTest(TestCase):

    def setUp(self): # filling user data (credentials)
        self.user = get_user_model().objects.create_user(
            username = 'yash',
            email = 'yashmarmat08@gmail.com',
            password = 'secret',
        )

        self.broker = Broker.objects.create(    # filling Broker model fields
            title = 'django for beginners',
            country = 'WS Vincent',
            description = 'anything',
            rate = '30',
            phone_number = '9920167677',
            image_url = 'https://forexample.jpg',
            broker_available = 'True',
        )

    def test_string_representation(self):
        broker = Broker(title='new Broker')
        self.assertEqual(str(broker), broker.title)

    def test_broker_model_fields_content(self):
        self.assertEqual(f'{self.broker.title}', 'django for beginners')
        self.assertEqual(f'{self.broker.country}', 'WS Vincent')
        self.assertEqual(f'{self.broker.description}', 'anything')
        self.assertEqual(f'{self.broker.rate}', '30')
        self.assertEqual(f'{self.broker.phone_number}', '9920167677')
        self.assertEqual(f'{self.broker.image_url}', 'https://forexample.jpg')
        self.assertEqual(f'{self.broker.broker_available}', 'True')

    def test_broker_list_view_for_logged_in_user(self):
        self.client.login(username = 'yash', email='yashmarmat08@gmail.com', password='secret')
        request = self.client.get(reverse('list'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_broker_list_view_for_anonymous_user(self): # a user who doesn't have an account on our site
        self.client.logout()
        request = self.client.get(reverse('list'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_broker_detail_view_for_logged_in_user(self):
        self.client.login(username = 'yash', email='yashmarmat08@gmail.com', password='secret')
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, 'WS Vincent')
        self.assertContains(request, '30')

    def test_broker_detail_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, 'WS Vincent')
        self.assertContains(request, '30')

    def test_checkout_view_for_logged_in_user(self):
        self.client.login(username = 'yash', email='yashmarmat08@gmail.com', password='secret')
        request = self.client.get(reverse('checkout', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_checkout_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('checkout', args='1'))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, '/accounts/login/?next=/1/checkout/') # redirects the user to login page

    def test_broker_when_available(self):  # a second broker is created (out of stock)
        request = self.client.get(reverse('detail', args = '1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Buy Now') 
        self.assertNotContains(request, 'Out of Stock !') # should not be there
        
    def test_broker_when_out_of_stock(self):  # a second broker is created which is out of stock
            broker = Broker.objects.create(
                title = 'new broker',
                country = 'yash',
                description = 'anything',
                rate = '30',
                phone_number = '9920167677',
                image_url = 'https://forexample.jpg',
                broker_available = 'False',   # out of stock when False
            )
            request = self.client.get(reverse('detail', args = '2'))
            self.assertEqual(request.status_code, 200)
            self.assertContains(request, 'Out of Stock !')
            self.assertNotContains(request, 'Buy Now') # buy now option is no longer present
  
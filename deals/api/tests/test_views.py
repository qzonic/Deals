import os
from decimal import Decimal

from django.db.models import Sum
from django.test import TestCase, Client


from api.models import Customer, Deal, Gem


class TestUploadDealView(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestUploadDealView, cls).setUpClass()
        cls.client = Client()
        cls.script_dir = os.path.dirname(__file__)

    def test_upload_data_with_bad_fields_names(self):
        file_path = os.path.join(self.script_dir, 'bad_customer_field.csv')
        with open(file_path, 'r') as file:
            response = self.client.post('', data={'deals': file})
            txt = response.json()[0]
            expected = {
                'customer': ['This field is required.'],
                'item': ['This field is required.'],
                'total': ['This field is required.'],
                'quantity': ['This field is required.'],
                'date': ['This field is required.']
            }
            self.assertEqual(txt, expected)

    def test_upload_without_file(self):
        response = self.client.post('')
        txt = response.json()
        expected = {'Error': 'Эндпоинт должен принимать csv файл'}
        self.assertEqual(txt, expected)

    def test_upload_deals(self):
        deals_count = Deal.objects.count()
        customer_count = Customer.objects.count()
        gem_count = Gem.objects.count()
        file_path = os.path.join(self.script_dir, 'deals.csv')
        with open(file_path, 'r') as file:
            response = self.client.post('', data={'deals': file})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'status': 'Success'})
            self.assertEqual(Deal.objects.count(), deals_count + 767)
            self.assertEqual(Customer.objects.count(), customer_count + 18)
            self.assertEqual(Gem.objects.count(), gem_count + 25)


class TestCustomerView(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCustomerView, cls).setUpClass()
        cls.client = Client()
        cls.script_dir = os.path.dirname(__file__)
        file_path = os.path.join(cls.script_dir, 'deals.csv')
        with open(file_path, 'r') as file:
            cls.client.post('', data={'deals': file})

    def test_get_customers(self):
        customers = Customer.objects.annotate(spent_money=Sum('deals__total')).order_by('-spent_money')[:5]
        response = self.client.get('')
        for response_customer, model_customer in zip(response.json()['response'], customers):
            self.assertEqual(response_customer['username'], model_customer.username)
            self.assertEqual(Decimal(response_customer['spent_money']), model_customer.spent_money)

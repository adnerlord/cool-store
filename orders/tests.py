from decimal import Decimal
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test.client import Client
from .models import Order, OrderItem
from shop.models import Product, Category


# Create your tests here.
class OrderCompleteTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name=u'Mouses'
        )
        self.product = Product.objects.create(
            category=self.category,
            name=u'Sensei',
            price=Decimal(99),
            stock=10,
            ordered=0,
        )
        self.order = Order.objects.create(
            first_name=u'fname',
            last_name=u'sname',
            email=u'test@test.mem',
            address=u'versh',
            postal_code=u'420420',
            city=u'tomsk',
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price,
        )
        self.password = u'mypassword'
        self.user = User.objects.create_superuser('myuser', 'test@test.ru', self.password)
        self.client = Client()
        self.client.post('/admin/login/?next=/admin/',
                         {'username': self.user.username,
                          'password': self.password})

    def test_order_creating(self):
        order = get_object_or_404(Order, id=self.order.id)
        self.assertEqual(order.get_total_cost(), Decimal(198.00))

    def test_order_pdf(self):
        order = get_object_or_404(Order, id=self.order.id)
        pdf_url = '/order/admin/order/{}/pdf/'.format(order.id)
        resp = self.client.get(pdf_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/order/pdf.html')

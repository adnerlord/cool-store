from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from shop.models import  Product
from .models import Order, OrderItem
from .views import AdminOrderCompete
from decimal import Decimal


# Create your tests here.
# class OrderCompleteTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.all()[0]
#         self.product = Product.objects.create(
#             name=u'Sensei',
#             price=Decimal(99),
#             stock=10,
#             ordered=0
#         )
#         self.order = Order.objects.create(
#             first_name=u'fname',
#             last_name=u'fname',
#             email=u'mem@mem.mem',
#             address=u'versh',
#             postal_code=u'420420'
#         )
#         self.order_item = OrderItem.objects.create(
#             order=self.order,
#             product=self.product,
#             quantity=2
#         )
#
#     def test_order_create(self, request):
#         url = reverse('orders:OrderCreate')
#         session = self.client.session
#         session['cart'] = 'test'
#         session.save()
#
#         user = self.user
#         resp = self.client.get(url)

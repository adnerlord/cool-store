from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

from cart import Cart


# Create your tests here.
# class CartViewTestCase(TestCase):
#     def setUp(self):
#         self.cart = Cart(request)

# class SimpleTest(TestCase):
#     def test_details(self):
#         self.client.get('/cart/')
#         cart = self.client.session.get(settings.CART_SESSION_ID)
#         print("############_1", type(cart), cart)
#         # print("############_2", type(cart['cart']), cart['cart'])
#         self.assertEqual(cart['cart'], "test")
#
# class Test1(TestCase):
#     def setUp(self):
#         self.client.get('/cart/')
#         session = self.client.session.get('cart')
#         request = add_session_to_request(session)
#         print("############_1", type(request), request)
#
#     def test_1(self):
#
#
#
# def add_session_to_request(request):
#     """Annotate a request object with a session"""
#     middleware = SessionMiddleware()
#     middleware.process_request(request)
#     request.session.save()
#     return request

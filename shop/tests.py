from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Product, Category
from decimal import Decimal


# Create your tests here.
class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=u'Mouses')
        self.product = Product.objects.create(
            category=self.category,
            name=u'Sensei',
            price=Decimal(99),
            stock=10,
            ordered=0
        )

    def test_product_adding(self):
        product = self.product

        self.assertEqual(product.name, u'Sensei')
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.price, Decimal(99))
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.ordered, 0)

    def test_category_slugify_and_unique(self):
        category = Category.objects.create(
            name=u'Mouses and NOTHING else')
        category2 = Category.objects.create(
            name=u'Mouses and NOTHING else')  # slug2 = mouses-and-nothing-else-2

        self.assertEqual(category.slug, u'mouses-and-nothing-else')
        self.assertTrue(category.slug != category2.slug)

    def test_detail_view(self):
        product = self.product

        # success product creation
        resp = self.client.get(product.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

        # success template using
        self.assertTemplateUsed(resp, 'shop/product/detail.html')

        # Error: ID don't match
        resp = self.client.get(reverse('shop:ProductDetail',
                                       args=[123, product.slug]))
        self.assertEqual(resp.status_code, 404)


from django.urls import reverse
from django.test import TestCase
from .models import Category, Restaurant, Product

class ProductViewTests(TestCase):

    def setUp(self):
        # Create test data
        self.category = Category.objects.create(name='Food', image='path/to/image.jpg')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Test Location',
            description='Test Description',
            image='path/to/restaurant_logo.jpg'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            image='path/to/product_image.jpg',
            category=self.category,
            restaurant_name=self.restaurant
        )

    def test_category_creation(self):
        # Test that the category was created successfully
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.name, 'Food')

    def test_restaurant_creation(self):
        # Test that the restaurant was created successfully
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(self.restaurant.name, 'Test Restaurant')

    def test_product_creation(self):
        # Test that the product was created successfully
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, 'Test Product')

    def test_show_main_view(self):
        # Ensure the main view returns a successful response
        response = self.client.get(reverse('Homepage:show_main'))
        self.assertEqual(response.status_code, 200)

    def test_restaurant_view(self):
        # Test the restaurant view for a specific restaurant
        response = self.client.get(reverse('Homepage:restaurant') + f'?restaurant_name={self.restaurant.name}')
        self.assertEqual(response.status_code, 200)

    def test_filter_product_view(self):
        # Test the filtering of products by category
        response = self.client.get(reverse('Homepage:filter_products') + '?category=Food')
        self.assertEqual(response.status_code, 200)

    def test_show_main_view_with_category_filter(self):
        # Test main view with category filtering
        response = self.client.get(reverse('Homepage:show_main') + '?category=Food')
        self.assertEqual(response.status_code, 200)

# To run this test, simply execute the command:
# python manage.py test Homepage

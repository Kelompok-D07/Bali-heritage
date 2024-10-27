from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from bookmarks.models import Bookmark
from Homepage.models import Category, Product, Restaurant
from django.core.files.uploadedfile import SimpleUploadedFile

class BookmarkViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.category = Category.objects.create(
            name="Food",
            image=SimpleUploadedFile("category.jpg", b"file_content", content_type="image/jpeg")
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Location",
            description="Description",
            image=SimpleUploadedFile("restaurant.jpg", b"file_content", content_type="image/jpeg")
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Product Description",
            price=10.00,
            category=self.category,
            restaurant_name=self.restaurant,
            image=SimpleUploadedFile("product.jpg", b"file_content", content_type="image/jpeg")
        )
        self.bookmark = Bookmark.objects.create(user=self.user, product=self.product)

    def test_show_bookmarks_view(self):
        response = self.client.get(reverse('bookmarks:show_bookmarks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks.html')
        self.assertContains(response, self.category.name)


    def test_delete_bookmarks_item_view(self):
        response = self.client.post(reverse('bookmarks:delete_bookmarks_item', args=[self.bookmark.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('removed', response.json()['status'])

    def test_filter_bookmarks_view(self):
        response = self.client.get(reverse('bookmarks:filter_bookmarks') + '?category=Food')
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json()['status'])

    def test_edit_notes_view(self):
        response = self.client.post(reverse('bookmarks:edit_notes', args=[self.bookmark.id]), {
            'notes': 'Updated Note'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json()['status'])
        self.bookmark.refresh_from_db()
        self.assertEqual(self.bookmark.notes, 'Updated Note')

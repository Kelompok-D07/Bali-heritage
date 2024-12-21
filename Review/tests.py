from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Review.models import Review
from Homepage.models import Restaurant
from Review.forms import ReviewForm
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid

class ReviewViewsTestCase(TestCase):
    def setUp(self):
        # Setup user dan restaurant
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Buat gambar dummy
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        
        # Tambahkan gambar ke restoran
        self.restaurant = Restaurant.objects.create(
            id=uuid.uuid4(),
            name="Test Restaurant",
            location="Test Location",
            description="Test Description",
            image=self.image
        )
        
        # Login user
        self.client.login(username="testuser", password="testpass")

        # Create initial review
        self.review = Review.objects.create(
            user=self.user,
            rating=4,
            comment="Great food!",
            restaurant=self.restaurant
        )
    
    def test_show_main_view(self):
        response = self.client.get(reverse('review:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main.html")

    def test_create_review_entry_view(self):
        response = self.client.post(reverse('review:create_review_entry', args=[self.restaurant.id]), {
            'rating': 5,
            'comment': 'Awesome place!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Review.objects.count(), 2)  # Ensure new review created

    def test_review_store_detail_view(self):
        response = self.client.get(reverse('review:review_store_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant.html')
        self.assertContains(response, "Great food!")

    def test_edit_review_view(self):
        response = self.client.post(reverse('review:edit_review', args=[self.review.id]), {
            'rating': 3,
            'comment': 'Updated comment'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after edit
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, 'Updated comment')

    def test_delete_review_view(self):
        response = self.client.post(reverse('review:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete
        self.assertEqual(Review.objects.count(), 0)  # Ensure review deleted

    def test_show_xml_view(self):
        response = self.client.get(reverse('review:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_view(self):
        response = self.client.get(reverse('review:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id_view(self):
        response = self.client.get(reverse('review:show_xml_by_id', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id_view(self):
        response = self.client.get(reverse('review:show_json_by_id', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_add_review_entry_ajax(self):
        response = self.client.post(reverse('review:add_review_entry_ajax', args=[self.restaurant.id]), {
            'comment': 'Delicious!',
            'rating': '5'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # Simulate AJAX
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], "success")
        self.assertIn('Delicious!', response_data['html'])  # Check that the HTML contains the comment


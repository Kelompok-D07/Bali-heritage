# forum/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Forum, Like
from Homepage.models import Restaurant
from django.utils import timezone
import uuid
import json

class ForumViewsTestCase(TestCase):
    def setUp(self):
        # Membuat pengguna
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        
        # Membuat restoran
        self.restaurant1 = Restaurant.objects.create(name='Restoran A')
        self.restaurant2 = Restaurant.objects.create(name='Restoran B')
        
        # Membuat forum
        self.forum1 = Forum.objects.create(
            title='Forum Pertama',
            content='Isi konten forum pertama',
            author=self.user1,
            created_at=timezone.now()
        )
        self.forum1.recommendations.set([self.restaurant1, self.restaurant2])
        
        self.forum2 = Forum.objects.create(
            title='Forum Kedua',
            content='Isi konten forum kedua',
            author=self.user2,
            created_at=timezone.now()
        )
        
        # Membuat like
        Like.objects.create(forum=self.forum1, user=self.user2)
        
        # Inisialisasi client
        self.client = Client()
    
    def test_forum_list_unauthenticated(self):
        response = self.client.get(reverse('forum:forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.forum1.title)
        self.assertContains(response, self.forum2.title)
        # Cek apakah 'has_liked' adalah False untuk pengguna tidak terautentikasi
        for forum in response.context['forums']:
            self.assertFalse(forum.has_liked)
    
    def test_forum_list_authenticated(self):
        self.client.login(username='user1', password='pass1234')
        response = self.client.get(reverse('forum:forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.forum1.title)
        self.assertContains(response, self.forum2.title)
        # Cek 'has_liked' untuk user1
        for forum in response.context['forums']:
            if forum == self.forum1:
                self.assertFalse(forum.has_liked)  # user1 belum like forum1
            elif forum == self.forum2:
                self.assertFalse(forum.has_liked)
    
    
    def test_like_post_authenticated(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:like_post', args=[self.forum1.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 2)  # Awalnya 1 like, ditambah 1
        
        # Cek apakah like sudah ditambahkan
        self.assertTrue(Like.objects.filter(forum=self.forum1, user=self.user1).exists())
        
        # Unliking
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['liked'])
        self.assertEqual(data['total_likes'], 1)
        
        # Cek apakah like sudah dihapus
        self.assertFalse(Like.objects.filter(forum=self.forum1, user=self.user1).exists())
    
    def test_like_post_unauthenticated(self):
        url = reverse('forum:like_post', args=[self.forum1.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Redirect ke login
        self.assertEqual(response.status_code, 302)
    
    def test_create_post_authenticated(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:create_post')
        data = {
            'title': 'Forum Baru',
            'content': 'Konten forum baru',
            'recommendations': [str(self.restaurant1.id), str(self.restaurant2.id)]
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        resp_data = json.loads(response.content)
        self.assertTrue(resp_data['success'])
        self.assertEqual(resp_data['post']['title'], 'Forum Baru')
        self.assertEqual(resp_data['post']['content'], 'Konten forum baru')
        self.assertEqual(len(resp_data['post']['recommendations']), 2)
        self.assertEqual(resp_data['post']['author'], 'user1')
        self.assertEqual(resp_data['post']['total_likes'], 0)
    
    def test_create_post_missing_fields(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:create_post')
        data = {
            'title': '',
            'content': 'Konten tanpa judul',
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.content)
        self.assertFalse(resp_data['success'])
        self.assertIn('error', resp_data)
    
    def test_create_post_invalid_recommendations(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:create_post')
        data = {
            'title': 'Forum Dengan Rekomendasi Invalid',
            'content': 'Konten',
            'recommendations': ['invalid-uuid']
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.content)
        self.assertFalse(resp_data['success'])
        self.assertIn('error', resp_data)
    
    def test_create_post_unauthenticated(self):
        url = reverse('forum:create_post')
        data = {
            'title': 'Forum Tanpa Login',
            'content': 'Konten',
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Redirect ke login
        self.assertEqual(response.status_code, 302)
    
    def test_get_post_authorized(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:get_post', args=[self.forum1.id])
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['post']['title'], self.forum1.title)
        self.assertEqual(data['post']['content'], self.forum1.content)
        self.assertEqual(len(data['post']['recommendations']), 2)
    
    def test_get_post_unauthorized(self):
        self.client.login(username='user2', password='pass1234')
        url = reverse('forum:get_post', args=[self.forum1.id])
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_edit_post_authorized(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:edit_post', args=[self.forum1.id])
        data = {
            'title': 'Forum Pertama Diedit',
            'content': 'Konten yang telah diedit',
            'recommendations': [str(self.restaurant1.id)]
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        resp_data = json.loads(response.content)
        self.assertTrue(resp_data['success'])
        self.assertEqual(resp_data['post']['title'], 'Forum Pertama Diedit')
        self.assertEqual(resp_data['post']['content'], 'Konten yang telah diedit')
        self.assertEqual(len(resp_data['post']['recommendations']), 1)
        
        # Cek di database
        self.forum1.refresh_from_db()
        self.assertEqual(self.forum1.title, 'Forum Pertama Diedit')
        self.assertEqual(self.forum1.content, 'Konten yang telah diedit')
        self.assertEqual(list(self.forum1.recommendations.all()), [self.restaurant1])
    
    def test_edit_post_unauthorized(self):
        self.client.login(username='user2', password='pass1234')
        url = reverse('forum:edit_post', args=[self.forum1.id])
        data = {
            'title': 'Tidak Boleh Edit',
            'content': 'Konten',
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
        resp_data = json.loads(response.content)
        self.assertFalse(resp_data['success'])
        self.assertIn('error', resp_data)
    
    def test_edit_post_invalid_data(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:edit_post', args=[self.forum1.id])
        data = {
            'title': '',
            'content': '',
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.content)
        self.assertFalse(resp_data['success'])
        self.assertIn('error', resp_data)
    
    def test_delete_post_authorized(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:delete_post', args=[self.forum1.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        resp_data = json.loads(response.content)
        self.assertTrue(resp_data['success'])
        
        # Cek apakah post sudah dihapus
        with self.assertRaises(Forum.DoesNotExist):
            Forum.objects.get(id=self.forum1.id)
    
    def test_delete_post_unauthorized(self):
        self.client.login(username='user2', password='pass1234')
        url = reverse('forum:delete_post', args=[self.forum1.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
        resp_data = json.loads(response.content)
        self.assertFalse(resp_data['success'])
        self.assertIn('error', resp_data)
    
    def test_delete_post_invalid_request(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('forum:delete_post', args=[self.forum1.id])
        response = self.client.get(url)  # Menggunakan GET bukan POST
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.content)
        self.assertFalse(resp_data['success'])
        self.assertIn('error', resp_data)
    
    def test_restaurant_search(self):
        url = reverse('forum:restaurant_search')
        response = self.client.get(url, {'q': 'Restoran', 'page': 1})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['results']), 2)
        self.assertTrue(data['pagination']['more'] == False)
    
    def test_restaurant_search_pagination(self):
        # Membuat lebih banyak restoran untuk menguji pagination
        for i in range(15):
            Restaurant.objects.create(name=f'Restoran {i+3}')
        
        url = reverse('forum:restaurant_search')
        response = self.client.get(url, {'q': 'Restoran', 'page': 1})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 10)
        self.assertTrue(data['pagination']['more'])
        
        response = self.client.get(url, {'q': 'Restoran', 'page': 2})
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 7)  # Total 17 restoran
        self.assertFalse(data['pagination']['more'])

    def test_highlight_text(self):
        from .views import highlight_text
        original_text = "Ini adalah contoh teks untuk dihighlight."
        search_query = "contoh"
        highlighted = highlight_text(original_text, search_query)
        expected = "Ini adalah <span class=\"bg-yellow-200\">contoh</span> teks untuk dihighlight."
        self.assertEqual(highlighted, expected)
    
    def test_highlight_text_case_insensitive(self):
        from .views import highlight_text
        original_text = "Ini adalah Contoh teks untuk dihighlight."
        search_query = "contoh"
        highlighted = highlight_text(original_text, search_query)
        expected = "Ini adalah <span class=\"bg-yellow-200\">Contoh</span> teks untuk dihighlight."
        self.assertEqual(highlighted, expected)
    
    def test_highlight_text_no_match(self):
        from .views import highlight_text
        original_text = "Tidak ada yang cocok di sini."
        search_query = "contoh"
        highlighted = highlight_text(original_text, search_query)
        expected = "Tidak ada yang cocok di sini."
        self.assertEqual(highlighted, expected)


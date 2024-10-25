from django.db import models
from django.contrib.auth.models import User
from Homepage.models import Product

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')  # Jika ingin mengaitkan dengan pengguna
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookmarks')
    notes = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal saat bookmark dibuat

    def __str__(self):
        return f"{self.user.username}'s bookmark - {self.product.name}"

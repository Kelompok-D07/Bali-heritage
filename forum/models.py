from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
    title = models.CharField(max_length=255) # judul forum
    content = models.TextField() # isi forum
    author = models.ForeignKey(User, on_delete=models.CASCADE) # penulis forum
    likes = models.ManyToManyField(User, related_name='forum_likes', blank=True) # Relasi ManyToMany ke model User untuk fitur "like"
    created_at = models.DateTimeField(auto_now_add=True) # waktu pembuatan forum
 
    def __str__(self):
        return self.title

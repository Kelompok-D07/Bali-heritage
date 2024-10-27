# forum/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape

class Forum(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    recommendations = models.ManyToManyField('Homepage.Restaurant', blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    @property
    def recommendations_list(self):
        if self.recommendations:
            return [rec.strip() for rec in self.recommendations.split(',') if rec.strip()]
        else:
            return []

class Like(models.Model):
    forum = models.ForeignKey(Forum, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('forum', 'user')

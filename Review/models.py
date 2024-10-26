from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
# Create your models here.
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField()
    comment = models.TextField()
    time = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.user.username} - {self.rating}'
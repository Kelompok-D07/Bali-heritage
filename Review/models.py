from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField()
    comment = models.TextField()
    image = models.ImageField()
    time = models.DateField(default=datetime.date.today)
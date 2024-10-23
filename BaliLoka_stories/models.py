from django.db import models

class Stories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()
    
    def __str__(self):
        return self.name
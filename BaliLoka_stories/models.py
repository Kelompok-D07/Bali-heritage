from django.db import models

class StoriesEntry(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
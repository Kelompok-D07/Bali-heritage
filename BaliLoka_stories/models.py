import uuid
from django.db import models

class StoriesEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = 'stories_image/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
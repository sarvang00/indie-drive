from django.db import models
from django.conf import settings

from datetime import datetime

class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    s3Uri = models.URLField(blank=True)
    is_public = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=datetime.now)
    shared = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="shared")
    def __str__(self):
        return self.name
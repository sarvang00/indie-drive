from django.db import models
from datetime import datetime
# from accounts.models import User

class File(models.Model):
    # owner = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    s3Uri = models.URLField(blank=True)
    is_public = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name
from django.db import models
from datetime import datetime

class ImageFile(models.Model):
    original = models.ImageField(upload_to='images/original/')
    result = models.ImageField(upload_to='images/result/')
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(auto_now=True)

from django.db import models
import uuid

class Keyword(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.text
    
from datetime import datetime

class News(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    # no = models.IntegerField()
    title = models.CharField(max_length=255)
    desc = models.TextField()
    img_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.title}'
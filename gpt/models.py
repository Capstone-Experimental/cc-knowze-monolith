from django.db import models
import uuid

class Keyword(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.text
    
class News(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    no = models.IntegerField()
    title = models.CharField(max_length=255)
    img_url = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.no} - {self.title}'
    
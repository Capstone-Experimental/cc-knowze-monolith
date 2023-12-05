from django.db import models
import uuid

class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    # fix
    # user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='courses')
    user = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    type_activity = models.CharField(max_length=100)
    theme_activity = models.CharField(max_length=100)
    desc = models.TextField()
    duration = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    avg_rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.title
    
class Subtitle(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    topic = models.CharField(max_length=100)
    shortdesc = models.TextField()
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='subtitles')
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.topic
    
class Content(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    opening = models.TextField()
    closing = models.TextField()
    subtitle = models.ForeignKey('courses.Subtitle', on_delete=models.CASCADE, related_name='contents')
    
    def __str__(self):
        return self.opening
    
class Steps(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    text = models.TextField()
    content = models.ForeignKey('courses.Content', on_delete=models.CASCADE, related_name='steps')
    
    def __str__(self):
        return self.text
    
class Feedback(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField()
    text = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return self.text
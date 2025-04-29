from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_image_file(value):
    import os
    ext = os.path.splitext(value.name)[1]  # Pobiera rozszerzenie pliku
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Nieobsługiwany format pliku. Dozwolone formaty: JPG, JPEG, PNG, GIF.')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
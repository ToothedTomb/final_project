import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from datetime import date

def logo_upload_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a random filename using UUID
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Return the path
    return os.path.join('logos/', filename)

class OperatingSystems(models.Model):
    name = models.CharField(max_length=200)
    Package_Manager = models.CharField(max_length=100)
    CPU_Architecture = models.CharField(max_length=200)
    Latest_Version = models.CharField(max_length=200)
    End_Of_Support = models.DateField(default=date.today)
    logo = models.ImageField(upload_to=logo_upload_path, blank=True, null=True)  # Use the function
    website = models.URLField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Operating Systems"
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    operating_system = models.ForeignKey(OperatingSystems, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('operating_system', 'user')  # One comment per user per OS
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.operating_system.name}"
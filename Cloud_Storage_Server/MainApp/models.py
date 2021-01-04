from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    # File
    file = models.FileField(blank=False, null=False)
    # Creator 
    #creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user = models.CharField(max_length=50, null=False, blank=True)
    # File extension
    extension = models.CharField(max_length=150, default=".txt") 
    # Photo file, depends on the file extension
    image = models.ImageField(default="file.jpg", null=True, blank=True)
    # Date and time of creation
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ALL FILES'
        verbose_name_plural = 'ALL FILES'
from django.db import models
from django.conf import settings

class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notice_files/', blank=True, null=True)
    viewcnt = models.IntegerField(default=0)
    mainphoto = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
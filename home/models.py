from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Goal(models.Model):
    title = models.CharField(max_length=20)
    amount = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='home/images/%Y/%m/%d/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/goal/{self.pk}'
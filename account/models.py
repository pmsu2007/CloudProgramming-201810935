from django.contrib.auth.models import User
from django.db import models, transaction


# Create your models here.

class Account(models.Model):
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('EXPENSE', '지출'),
        ('INCOME', '수입')
    )
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    title = models.CharField(max_length=20)
    amount = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/account/{self.pk}'


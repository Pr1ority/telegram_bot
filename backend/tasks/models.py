import secrets

from django.db import models
from django.contrib.auth.models import User


def generate_id():
    return secrets.token_hex(8)


class Category(models.Model):
    id = models.CharField(
        primary_key=True, max_length=16, default=generate_id, editable=False
    )
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(
        primary_key=True, max_length=16, default=generate_id, editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

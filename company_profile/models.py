from django.db import models

# Create your models here.

class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self) -> str:
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.name
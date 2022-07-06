from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.BooleanField()
    birth = models.DateField()


class PhoneNumber(models.Model):
    number = models.TextField(
        unique=False
    )

    class Meta:
        ordering = ('number',)


class Person(models.Model):
    surname = models.TextField(
        unique=True
    )
    phone = models.ManyToManyField(PhoneNumber)

    class Meta:
        ordering = ('surname', )

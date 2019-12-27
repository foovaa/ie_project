from django.db import models
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
# Create your models here.

class Employees(models.Model):
    STATUS_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('none', 'None'),
    )
    
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    national_id = models.CharField(unique=True, max_length=10)
    personal_id = models.CharField(primary_key=True, max_length=10)
    tele = PhoneNumberField(null=True, unique=True, blank=False)
    address = models.CharField(max_length=200)
    salary = models.PositiveIntegerField()
    age = models.SmallIntegerField(null=False, default=0)
    is_married = models.BooleanField(default=False)
    gender = models.CharField(max_length=6, choices=STATUS_CHOICES, default='none')
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    objects = models.Manager()




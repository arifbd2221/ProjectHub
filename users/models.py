from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):

    gender_list = (('malle', 'Male'), ('female', 'Female'),)
    dept_list = (('swe','Software Engineering'),('cse', 'Computer Science Engineering'),('eee', 'Electronics & Electrical Engineering'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_areas = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=gender_list, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=20, choices=dept_list, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return 'Profile'

class Message(models.Model):
    content = models.TextField(('Content'))
    sender = models.ForeignKey(User, related_name='sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received', on_delete=models.CASCADE)

    def __str__(self):
        return self.content
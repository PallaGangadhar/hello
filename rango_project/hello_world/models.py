from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    cat = models.ForeignKey(category,on_delete=id) 
    title = models.CharField(max_length=128) 
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self): # For Python 2, use __unicode__ too 
        return self.title

class student(models.Model):
    erno= models.IntegerField(unique=True)
    name = models.CharField(max_length=128,unique=True)
    city = models.CharField(max_length=128)
    dob=models.CharField(max_length=128)
    email=models.EmailField(max_length=128,unique=True)
    phone=models.IntegerField(unique=True)

    def __str__(self):
        return self.erno
        return self.name
        #return self.dob,self.email,
        #return self.phone
        


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=True)
    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username


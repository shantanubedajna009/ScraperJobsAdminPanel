from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import User


class UserInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)

    picture = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class Added_Jobs(models.Model):
    date_created = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, blank=True)
    run_status = models.CharField(max_length=200, default='1')
    excluded_sellers = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.email


class Check_Ads_One(models.Model):
    title = models.CharField(max_length=200, blank=True)
    price = models.CharField(max_length=200, blank=True)
    seller_name = models.CharField(max_length=200, blank=True)
    listing_date = models.CharField(max_length=200, blank=True)
    listing_location = models.CharField(max_length=200, blank=True)
    paragraph = models.TextField(blank=True)
    list_attributes = models.CharField(max_length=200, blank=True)
    image_link = models.CharField(max_length=200, blank=True)
    prod_link = models.CharField(max_length=200, blank=True)

class Check_Ads_Two(models.Model):
    title = models.CharField(max_length=200, blank=True)
    price = models.CharField(max_length=200, blank=True)
    seller_name = models.CharField(max_length=200, blank=True)
    listing_date = models.CharField(max_length=200, blank=True)
    listing_location = models.CharField(max_length=200, blank=True)
    paragraph = models.TextField(blank=True)
    list_attributes = models.CharField(max_length=200, blank=True)
    image_link = models.CharField(max_length=200, blank=True)
    prod_link = models.CharField(max_length=200, blank=True)

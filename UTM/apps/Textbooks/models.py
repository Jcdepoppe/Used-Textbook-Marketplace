from __future__ import unicode_literals
from django.db import models
import re
import datetime
import calendar

from apps.log_reg.models import User


class Book(models.Model):
    title = models.CharField(max_length = 255)
    edition = models.SmallIntegerField()
    publisher = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    ISBN = models.BigIntegerField(default=0)
    cover = models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Sells(models.Model):
    seller = models.ForeignKey(User, related_name='sells')
    book = models.ForeignKey(Book, related_name='for_sale')
    condition = models.SmallIntegerField()
    price = models.IntegerField(null=True)
    picture = models.ImageField(blank=True, null=True, upload_to='user_pics/', verbose_name="", default="No-pic.png")
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wants(models.Model):
    buyer = models.ForeignKey(User, related_name='wants')
    book = models.ForeignKey(Book, related_name='wanted')
    condition = models.SmallIntegerField()
    price = models.IntegerField(null=True)
    distance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    content = models.TextField()
    posted_by = models.ForeignKey(User, related_name='messages')
    on_book = models.ForeignKey(Sells, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    on_message = models.ForeignKey(Message, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

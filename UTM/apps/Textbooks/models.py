from __future__ import unicode_literals
from django.db import models
import re
import datetime
import calendar

from apps.log_reg.models import User

class Book(models.Model):
    title = models.CharField(max_length = 255)
    publisher = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    ISBN = models.CharField(max_length = 13, default="0")
    cover = models.CharField(max_length=255, default="https://goo.gl/7vbrVt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Sells(models.Model):
    seller = models.ForeignKey(User, related_name='sells')
    book = models.ForeignKey(Book, related_name='for_sale')
    condition = models.SmallIntegerField()
    price = models.IntegerField(null=True)
    picture = models.ImageField(blank=True, null=True, upload_to='user_pics/', verbose_name="", default="/user_pics/No_pic.png")
    description = models.TextField(null=True)
    sold = models.BooleanField(default=False)
    buyer_email = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def actual_price(self):
        return self.price/100

    def display_price(self):
        actual_price = self.price/100
        dollars = '${:,.2f}'.format(actual_price)
        return dollars
        
    def __str__(self):
        mod_title=self.book.title
        if self.sold:
            mod_title += " <span class='badge badge-warning'>SOLD</span>"
        return mod_title

class Wants(models.Model):
    buyer = models.ForeignKey(User, related_name='wants')
    book = models.ForeignKey(Book, related_name='wanted')
    condition = models.SmallIntegerField()
    price = models.IntegerField(null=True)
    distance = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def actual_price(self):
        return self.price/100

    def display_price(self):
        actual_price = self.price/100
        dollars = '${:,.2f}'.format(actual_price)
        return dollars
    # def __repr__(self):
    #     return "{}" .format(self.book)


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

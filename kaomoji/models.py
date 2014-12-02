from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    category = models.ForeignKey(Category)

class Emoticon(models.Model):
    content = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory, null=True)
    index = models.IntegerField(null=True)

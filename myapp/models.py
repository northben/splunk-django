from django.db import models


class MyModel(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
    foo = models.CharField(max_length=255, default='')

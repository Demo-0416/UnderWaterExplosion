from django.db import models


# Create your models here.
class History(models.Model):
    save_time = models.CharField(max_length=100)
    exp_name = models.CharField(max_length=100)
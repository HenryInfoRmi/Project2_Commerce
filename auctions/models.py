from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class auct_list(models.Model):
    name_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    name_act = models.CharField(max_length=100)
    price_act = models.FloatField()
    picture_act = models.ImageField(upload_to="media/", blank=True)
    date_act = models.DateTimeField()
    desc_act = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name_act}, {self.price_act}, {self.picture_act}, {self.date_act}, {self.desc_act}"

class bid(models.Model):
    name_prod = models.ForeignKey(auct_list, on_delete=models.CASCADE, related_name="product")
    name_bid = models.CharField(max_length=64)
    price_bid = models.FloatField()
    date_bid = models.DateTimeField()
    def __str__(self):
        return f"{self.name_bid}, {self.price_bid}, {self.date_bid}"

class comment_auct(models.Model):
    name_prod = models.ForeignKey(auct_list, on_delete=models.CASCADE, related_name="post_product")
    name_commenter = models.CharField(max_length=64)
    comment = models.CharField(max_length=400)
    date_comment = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return f"{self.name_commenter}: {self.comment} {self.date_comment}"
from asyncio.windows_events import NULL
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id          = models.AutoField(primary_key=True)
    username    = models.CharField('username', max_length=20, unique=True)
    password    = models.CharField('password', max_length=256)
    email       = models.EmailField('email', max_length=100)


class Category(models.Model):
    id              = models.AutoField(primary_key=True)
    name   = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Listing(models.Model):
    id              = models.AutoField(primary_key=True)
    user_id         = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    title           = models.CharField(max_length=100, blank=False)
    description     = models.TextField(max_length=400)
    image_url       = models.URLField()
    creation_date   = models.DateTimeField(auto_now_add=True, blank=True)
    is_active       = models.BooleanField(default=True)
    category_id     = models.ForeignKey(Category, related_name='categorys', on_delete=models.DO_NOTHING)
    initial_bid     = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    def __str__(self):
        return self.title


class Watchlist(models.Model):
    id                = models.AutoField(primary_key=True)
    user_id           = models.ForeignKey(User, related_name='watchlists', on_delete=models.CASCADE)
    listing_id        = models.ForeignKey(Listing, related_name='watched_list', on_delete=models.CASCADE)


class Comments(models.Model):
    id              = models.AutoField(primary_key=True)
    user            = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    listing         = models.ForeignKey(Listing, related_name='listing_comments', on_delete=models.CASCADE)
    comment         = models.TextField(max_length=300)
    comment_date    = models.DateTimeField(auto_now_add=True, blank=True)


class Bid(models.Model):
    id          = models.AutoField(primary_key=True)
    listing_id  = models.ForeignKey(Listing, related_name='bid_listings', on_delete=models.CASCADE)
    user_id     = models.ForeignKey(User, related_name='bid_users', on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    bid_date    = models.DateTimeField(auto_now_add=True, blank=True)
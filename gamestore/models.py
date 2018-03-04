from django.db import models
from django.contrib.auth.models import User
import datetime
import random, string
from django.core.mail import send_mail
from .settings import SERVICE_URL
from social_django.models import UserSocialAuth
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    genreID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return str(self.name)


class Game(models.Model):
    gameID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(validators=[MaxValueValidator(1000.0), MinValueValidator(0.0)])
    publishDate = models.DateTimeField(auto_now=True)
    url = models.URLField()
    genreID = models.ForeignKey(Genre, on_delete=models.PROTECT)
    developerID = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField()
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ('-publishDate',)

    def __str__(self):
        return str(self.name)


class GameStats(models.Model):
    statID = models.AutoField(primary_key=True)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    gameID = models.ForeignKey(Game, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    gamestate = models.TextField(default='')

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return str(self.statID)


class GamePurchase(models.Model):
    purchaseID = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    cost = models.FloatField()
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    sellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    gameID = models.ForeignKey(Game, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return str(self.purchaseID)


class UserAttributes(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    isDeveloper = models.BooleanField(default=False)
    verificationToken = models.CharField(max_length=64)


def createUserAttributes(instance, created, raw, **kwargs):
    if not created or raw:
        return
    
    userID = instance

    token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
    attributes = UserAttributes.objects.create(userID=userID,
                                               verificationToken=token)
    attributes.save()

    if userID.is_staff == False:
        userID.is_active = False
        send_mail(
            'Verify your account',
            'Please verify your account "{}" by clicking this link: '.format(userID.username) +
            SERVICE_URL + '/account/verify/{}'.format(token) + '/',
            'gamestore@gamestore.com',
            [userID.email]
        )

    instance.save()

def activateUser(instance, created, raw, **kwargs):
    print('Activate')
    if not created or raw:
        return
    
    userID = instance.user
    userID.is_active = True
    userID.save()

models.signals.post_save.connect(createUserAttributes, sender=User, dispatch_uid='createUserAttributes')
models.signals.post_save.connect(activateUser, sender=UserSocialAuth, dispatch_uid='activateUser')
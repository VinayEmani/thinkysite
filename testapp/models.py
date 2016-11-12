from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

import pytz

# Create your models here.

class ThinkyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='pics/', blank=True)
    is_mod = models.BooleanField(default=False)
    timezones = [(x, x) for x in pytz.all_timezones]
    timezone = models.CharField(max_length=50,
                                choices=timezones,
                                default='UTC')

    def __str__(self):
        return '%s\'s profile' % self.user.username

@receiver(post_save, sender=User)
def create_thinky_user(sender, instance, created, **kwargs):
    if created:
        ThinkyUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_thinky_user(sender, instance, **kwargs):
    instance.thinkyuser.save()

class Board(models.Model):
    board_name = models.CharField(max_length=200)
    board_desc = models.CharField(max_length=500)

    def __str__(self):
        return self.board_name

class SubForum(models.Model):
    # sub forum name, sub forum brief desc, 
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    forum_name = models.CharField(max_length=200)
    forum_desc = models.CharField(max_length=500)

    def __str__(self):
        return self.forum_name

class Thread(models.Model):
    sub_forum = models.ForeignKey(SubForum, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField()
    thread_type = models.IntegerField(default=0)
    last_post_time = models.DateTimeField(
            default=datetime(year=1980, month=1, day=1))
    num_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField()

    def __str__(self):
        return 'Thread #%s' % self.id

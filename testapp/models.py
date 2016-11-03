from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class ThinkyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='pics/', blank=True)

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

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField()

    def __str__(self):
        return 'Thread #%s' % self.id

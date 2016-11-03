from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ThinkyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='pics/') 

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

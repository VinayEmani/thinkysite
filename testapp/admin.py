from django.contrib import admin

from .models import ThinkyUser, Thread, Comment, Board, SubForum
# Register your models here.

admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Board)
admin.site.register(SubForum)
admin.site.register(ThinkyUser)

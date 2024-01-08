from django.contrib import admin
from .models import User , Post , Comment , Mention , GroupPost, GroupComment


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Mention)
admin.site.register(GroupPost)
admin.site.register(GroupComment)

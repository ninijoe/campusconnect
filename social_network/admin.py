from django.contrib import admin
from .models import User , Post , Comment , Mention , GroupPost, GroupComment, JoinRequest


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Mention)
admin.site.register(GroupPost)
admin.site.register(GroupComment)
admin.site.register(JoinRequest)


from django.contrib import admin
from .models import (Post, Category, Tag, PostComment, PostCommentReplay)

admin.site.register(Post),
admin.site.register(Category),
admin.site.register(Tag),
admin.site.register(PostComment),
admin.site.register(PostCommentReplay),
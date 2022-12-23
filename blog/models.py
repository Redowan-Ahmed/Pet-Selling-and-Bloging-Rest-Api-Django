from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class BaseModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.category_name

    def save(self, *args, **kwargs):
        unique_code = str(uuid.uuid4()).split('-')
        self.slug = slugify(self.category_name) + '-' + unique_code[0]
        return super(Category, self).save(*args, **kwargs)


class Tag(BaseModel):
    tag_title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.tag_title


class Post(BaseModel):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    featured_image = models.ImageField(upload_to='uploads/postsimages', blank=True, null=True)
    category = models.ForeignKey(
        Category, models.SET_DEFAULT, default='uncategorized', related_name='category')
    tag = models.ManyToManyField(Tag, related_name='tag')
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    slug = models.SlugField(max_length=350, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        unique_code = str(uuid.uuid4()).split('-')
        self.slug = slugify(self.title) + '-' + unique_code[0]
        return super(Post, self).save(*args, **kwargs)

    def increaseViews(self):
        self.views += int(1)
        self.save()

    def increaseLikes(self):
        self.likes += int(1)
        self.save()


class PostComment(BaseModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return f"' {self.title} ' is commented on post {self.post.title}"


class PostCommentReplay(BaseModel):
    post_comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="post_comment_reply")
    reply = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"'{self.reply}' replied in comment {self.post_comment.title}"

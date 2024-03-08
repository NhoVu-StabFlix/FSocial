from django.db import models
from userauths.models import User, Profile, user_directory_path
from django.utils.text import slugify
from django.utils.html import format_html
from shortuuid.django_fields import ShortUUIDField
import shortuuid

VISIBILITY = (
    ("Only Me", "Only Me"),
    ("Everyone", "Everyone")
)

FRIEND_REQUEST = (
    ("pending", "pending"),
    ("accept", "accept"),
    ("Cancel", "Cancel")
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=100, choices=VISIBILITY, default='Everyone')
    pid = ShortUUIDField(length=10, max_length=25, alphabet='1234567890')
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        else:
            return "No Image"

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.title) + "-" + uniqueid
        super(Post, self).save(*args, **kwargs)


class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery', null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)

    class Meta:
        verbose_name_plural = 'Gallery'

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        else:
            return "No Image"


class Friend(models.Model):
    friends_id = ShortUUIDField(length=10, max_length=20, alphabet='0123456789')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.friend)

    class Meta:
        verbose_name_plural = 'Friends'


class FriendRequest(models.Model):
    friend_request_id = ShortUUIDField(length=10, max_length=25, alphabet='0123456789')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_request')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receive_friend_request')
    status = models.CharField(max_length=100, default='pending', choices=FRIEND_REQUEST)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)

    class Meta:
        verbose_name_plural = 'Request Friend'


class Comment(models.Model):
    comment_id = ShortUUIDField(length=10, max_length=25, alphabet='0123456789')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    comment_content = models.CharField(max_length=1000, default='')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.comment_content)

    class Meta:
        verbose_name_plural = 'Comment'


class ReplyComment(models.Model):
    reply_comment_id = ShortUUIDField(length=10, max_length=25, alphabet='0123456789', )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply_post')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply_comment')
    reply_content = models.CharField(max_length=1000, )
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='replay_comment_likes')

    def __str__(self):
        return str(self.reply_content)

    class Meta:
        verbose_name_plural = 'Reply Comment'

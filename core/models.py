import shortuuid
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField

from userauths.models import User, Profile, user_directory_path

VISIBILITY = (
    ("Only Me", "Only Me"),
    ("Everyone", "Everyone")
)

FRIEND_REQUEST = (
    ("pending", "pending"),
    ("accept", "accept"),
    ("Cancel", "Cancel")
)
NOTIFICATION_TYPE = (
    ("Friend Request", "Friend Request"),
    ("Friend Request Accept", "Friend Request Accept"),
    ("New Followers", "New Followers"),
    ("New Like", "New Like"),
    ("Comment Liked", "Comment Liked"),
    ("Comment Replied", "Comment Replied"),
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

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-date']

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


class Notification(models.Model):
    notification_id = ShortUUIDField(length=10, max_length=25, alphabet='0123456789')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notification_post', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_notification', blank=True,
                                null=True)
    notification_type = models.CharField(max_length=255, choices=NOTIFICATION_TYPE)
    notification_content = models.CharField(max_length=500, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Notification'


class Group(models.Model):
    group_id = ShortUUIDField(length=10, max_length=20, alphabet='0123456789')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_user')
    members = models.ManyToManyField(User, related_name='group_members', max_length=255)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    video = models.FileField(max_length=255, blank=True, null=True)
    visibility = models.CharField(max_length=255, choices=VISIBILITY, default='Everyone')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name) + "-" + uuid_key

        super(Group, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        else:
            return "No Image"


class GroupPost(models.Model):
    group_post_id = ShortUUIDField(length=10, max_length=25, alphabet='0123456789')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='post_group')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_group_user')
    title = models.CharField(max_length=255, blank=True, null=True)
    group_post_content = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(max_length=100, upload_to=user_directory_path, blank=True, null=True)
    video = models.FileField(max_length=100, blank=True, null=True, upload_to=user_directory_path)
    visibility = models.CharField(max_length=255, choices=VISIBILITY, default='everyone')
    likes = models.ManyToManyField(User, blank=True, related_name='group_post_likes')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title) + "-" + uuid_key
        super(GroupPost, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        else:
            return "No Image"


class Page(models.Model):
    page_id = ShortUUIDField(length=10, max_length=20, alphabet='0123456789')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_user')
    followers = models.ManyToManyField(User, related_name='page_followers')
    likes = models.ManyToManyField(User, related_name='page_likes', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(max_length=255, upload_to=user_directory_path, blank=True, null=True)
    video = models.FileField(max_length=255, blank=True, null=True, upload_to=user_directory_path)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    visibility = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name) + '-' + uuid_key

        super(Page, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        else:
            return "No Image"


class PagePost(models.Model):
    page_post_id = ShortUUIDField(length=10, max_length=25, alphabet='0123456789')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='post_page')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_page_user')
    title = models.CharField(max_length=255, blank=True, null=True)
    page_post_content = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(max_length=255, blank=True, null=True, upload_to=user_directory_path)
    video = models.FileField(max_length=255, blank=True, null=True, upload_to=user_directory_path)
    visibility = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='post_page_likes')
    active = models.BooleanField(default=True)
    slug = models.CharField(unique=True, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title) + '-' + uuid_key

        super(PagePost, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        else:
            return "No Image"

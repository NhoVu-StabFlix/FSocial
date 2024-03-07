from django.db import models
from userauths.models import User, Profile, user_directory_path
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid

VISIBILITY = (
    ("Only Me", "Only Me"),
    ("Everyone", "Everyone")
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=100, choices=VISIBILITY, default='Everyone')
    pid = ShortUUIDField(length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvwxyz')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.title) + "-" + uniqueid

        super(Post, self).save(*args, **kwargs)

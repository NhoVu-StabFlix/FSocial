from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from shortuuid.django_fields import ShortUUIDField
from shortuuid import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)
RELATIONSHIP = (
    ('signle', 'Single'),
    ('married', 'Married'),
)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user_id, ext)
    return "user_{0}/{1}".format(instance.user_id, filename)


class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200)
    email = models.CharField(unique=True, max_length=200)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER,default='Male')
    otp = models.CharField(max_length=10, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # Create your models here.


class Profile(models.Model):
    pid = ShortUUIDField(length=11, max_length=25, prefix='1000', alphabet='0123456789')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to=user_directory_path, default='cover.jpg')
    images = models.CharField(user_directory_path, max_length=200, default='default.jpg')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, choices=GENDER, default='Male')
    relationship = models.CharField(max_length=200, choices=RELATIONSHIP, default='Single')
    about_me = models.TextField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    working_at = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)
    follower = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    blocked = models.ManyToManyField(User, blank=True, related_name='blocked')
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            uuid_key = uuid()
            uniqueid = uuid_key[:2]
            if self.full_name:
                self.slug = slugify(self.full_name + "-" + str(uniqueid))
            else:
                self.slug = slugify(str(self.pid))
        else:

            uuid_key = uuid()
            uniqueid = uuid_key[:2]
            if self.full_name:
                self.slug = slugify(self.full_name + "-" + str(uniqueid))

        super(Profile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

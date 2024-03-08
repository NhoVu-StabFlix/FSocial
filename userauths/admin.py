from django.contrib import admin
from userauths.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'gender')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['slug', 'full_name', 'user', 'verified', ]
    list_editable = ['verified', ]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)

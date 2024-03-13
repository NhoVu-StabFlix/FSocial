from django.contrib import admin
from core.models import Post, Gallery, Friend, FriendRequest, Comment, ReplyComment, Notification, Group, Page, \
    GroupPost, PagePost


class GalleryAdminTab(admin.TabularInline):
    model = Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "post", "active"]


class PostAdmin(admin.ModelAdmin):
    inlines = [GalleryAdminTab]
    list_display = ['thumbnail', 'user', 'title', 'visibility', 'active']
    list_editable = ['active']
    prepopulated_fields = {"slug": ("title",)}


class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', ]


class FriendRequestAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['sender', 'receiver', 'status']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment_content', 'active']


class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'reply_content', 'comment', 'post']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'notification_content', 'is_read']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'name', 'description', 'visibility', 'active', 'date']
    list_editable = ['name', 'description', 'visibility']
    prepopulated_fields = {"slug": ["name", ], }


class GroupPostAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'group_post_content', 'visibility']
    prepopulated_fields = {"slug": ["title", ], }


class PageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'name', 'description', 'visibility', 'date']
    list_editable = ['name', 'description', 'visibility']


class PagePostAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'page_post_content', 'date']


admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GroupPost, GroupPostAdmin)
admin.site.register(PagePost, PagePostAdmin)

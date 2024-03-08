from django.contrib import admin
from core.models import Post, Gallery, Friend, FriendRequest, Comment, ReplyComment


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


admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)

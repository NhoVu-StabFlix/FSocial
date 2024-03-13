import shortuuid
from django.shortcuts import render
from django.utils.text import slugify
from core.models import Post
from django.http import JsonResponse
from django.utils.timesince import timesince


def index(request):
    posts = Post.objects.filter(active=True, visibility='Everyone')
    context = {
        "posts": posts
    }
    return render(request, 'core/feed.html', context)


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get("post-caption")
        visibility = request.POST.get("visibility")
        image = request.POST.get("post-thumbnail")
        print("title ", title)
        print("visibility ", visibility)
        print("image ", image)

        uuidkey = shortuuid.uuid()
        if title and image:
            slug = slugify(title) + "-" + uuidkey
            post = Post(title=title, visibility=visibility, image=image, user=request.user, slug=slug)
            post.save()
            return JsonResponse(
                {
                    'post': {
                        'title': post.title,
                        'image': post.image,
                        'full_name': post.user.profile.full_name,
                        'profile_image': post.user.profile.images,
                        'date': timesince(post.date),
                        'id': post.id
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'error': 'Please fill all the fields'
                }
            )
    return JsonResponse({"data": "sent"})

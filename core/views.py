import shortuuid
from django.shortcuts import render, redirect, reverse
from django.utils.text import slugify
from core.models import Post
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    posts = Post.objects.filter(active=True, visibility='Everyone')
    context = {
        "posts": posts
    }
    return render(request, 'core/feed.html', context)


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')

        print("Title ============", title)
        print("thumbnail ============", image)
        print("visibility ============", visibility)

        uuid_key = shortuuid.uuid()

        if title and image:
            slug = slugify(title) + "-" + uuid_key
            post = Post(title=title, image=image, visibility=visibility, user=request.user,
                        slug=slug)
            post.save()

            return JsonResponse(
                {'post':
                    {
                        'title': post.title,
                        'image_url': post.image.url,
                        "full_name": post.user.profile.full_name,
                        "profile_image": post.user.profile.images.url,
                        "date": timesince(post.date),
                        "id": post.id,
                    }}
            )

        else:
            return JsonResponse({'error': 'Invalid post data'})

    return JsonResponse({'data': 'sent'})


@login_required()
def like_post(request):
    post_id = request.GET['id']
    post = Post.objects.get(id=post_id)
    user = request.user
    is_liked = False
    if user in post.likes.all():
        is_liked = False
        post.likes.remove(user)
    else:
        is_liked = True
        post.likes.add(user)

    data = {
        "is_liked": is_liked,
        "likes": Post.objects.get(id=post_id).likes.count()
    }
    return JsonResponse({"data": data})

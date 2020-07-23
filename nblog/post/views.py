import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import PostForm
from .models import Post

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def posts_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    post_list = [{"id":x.id, "content": x.content, "likes":random.randint(0, 1110) } for x in qs ]

    data = {
        "response": post_list
    }
    return JsonResponse(data)
    # return render(request, "post/list.html")

def post_create_view(request, *arg, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = PostForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = PostForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'post/components/forms.html', context={"form":form})

def posts_detail_view(request, post_id, *args, **kwargs):
    data = {
        "id":post_id,
    }
    status = 200    
    try:
        obj = Post.objects.get(id=post_id)
        data['content'] = obj.content
        # data['user'] = obj.user
    except:
        data['message'] = "Not found"
        status = 400

        # raise Http404
    return JsonResponse(data, status=status)
    

    # return HttpResponse(f"<h1>Hello -{post_id} --{obj.content} --{obj.user} </h1>")


    # return render(request, "post/detail.html", context={"post_id": post_id})

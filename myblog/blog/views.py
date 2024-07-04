import logging
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pytz

logger = logging.getLogger(__name__)

def post_list(request):
    posts = Post.objects.all().order_by('-pinned', '-created_at')
    now = timezone.now()
    logger.info(f"Current Time (Django): {now}")
    return render(request, 'home.html', {'posts': posts})

def post_new(request):
    now = timezone.now()
    logger.info(f"Current Time (Django): {now}")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = now
            post.updated_at = now
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@csrf_exempt
def post_edit_ajax(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')

        post = get_object_or_404(Post, pk=post_id)
        post.content = content
        post.updated_at = timezone.now()
        post.save()

        ist = pytz.timezone('Asia/Kolkata')
        updated_at_ist = post.updated_at.astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')

        return JsonResponse({
            'content': post.content,
            'updated_at': updated_at_ist
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def pin_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.pinned = True
        post.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def unpin_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.pinned = False
        post.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
            post.delete()
            return JsonResponse({'success': True})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog')
        else:
            return render(request, 'signin.html', {'error': 'Invalid credentials'})
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('blog')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def blog(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'blog.html', {'posts': posts})

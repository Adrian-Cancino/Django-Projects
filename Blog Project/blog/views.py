from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

from .models import Post, Comments
from .forms import CommentForm
# Create your views here.

def post_list(request):

    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        post = paginator.page(page_number)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        post = paginator.page(1)

    return render(request,
                  'blog/post/list.html',
                  {'posts': post})

def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)
    
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    #A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Creat a comment object without saving in the database
        comment = form.save(commit=False)
        # Assign the post to a comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    return render(request, 'blog/post/comment.html',{
        'post': post,
        'form': form,
        'comment': comment
    })

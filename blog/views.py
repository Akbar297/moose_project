from django.shortcuts import render, redirect
from blog.models import Post, Contact, Comment


def home_view(request):
    posts = Post.objects.filter(is_published=True)
    d = {
        'posts': posts,
        'home': 'active'
    }
    return render(request, 'index.html', context=d)


def blog_view(request):
    data = request.GET
    cat = data.get('cat', None)
    if cat:
        posts = Post.objects.filter(is_published=True, category_id=cat)
    else:
        posts = Post.objects.filter(is_published=True)

    d = {
        'posts': posts,
        'blog': 'active'
    }
    return render(request, 'blog.html', context=d)


def blog_detail_view(request, id):
    if request.method == 'POST':
        data = request.POST
        comment = Comment.objects.create(post_id=id, name=data['name'], email=data['email'], message=data['message'])
        comment.save()
        return redirect(f'/blog/{id}/')
    post = Post.objects.filter(id=id).first()
    comments = Comment.objects.filter(post_id=id, is_visible=True)
    d = {'comments': comments, 'post': post, 'comments_count': len(comments), 'blog': 'active'}
    return render(request, 'blog-single.html', context=d)


def about_view(request):
    return render(request, 'about.html', context={'about': 'active'})


def contact_view(request):
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(full_name=data['name'], email=data['email'],
                                     subject=data['subject'], message=data['message'])
        obj.save()
        return redirect('/contact')
    return render(request, 'contact.html', {'contact': 'active'})

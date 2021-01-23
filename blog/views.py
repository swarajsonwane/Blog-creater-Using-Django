from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm,SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector   #for searching purpose



from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required




from django.shortcuts import HttpResponseRedirect


class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        if not request.user.is_authenticated():
            return HttpResponseRedirect('login')

        # Code to be executed for each request/response after
        # the view is called.

        return response

def  post_share(request,pk):
    post = get_object_or_404(Post,pk=pk,status='published')
    sent=False
    if request.method=='POST':
        #form was submitted
        form =EmailPostForm(request.POST)
        if form.is_valid():
            #form field passed validation
            cd = form.cleaned_data
            #..send email
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'swarajsonwane1604@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                  'form':form})



class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request,tag_slug=None):
    object_list = Post.objects.all()
    tag=None

    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])

    paginator=Paginator(object_list,3) #3 post per page
    page=request.GET.get('page')      #number of current page
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #if page not integer deliver first page
        posts=paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page
        posts=paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'page':page,
                   'tag':tag})


def post_detail(request, pk):
    # post = get_object_or_404(Post, slug=post,
    #                                status='published',
    #                                publish__year=year,
    #                                publish__month=month,
    #                                publish__day=day)
    post=get_object_or_404(Post,pk=pk)

    comments=post.comments.filter(active=True)

    new_comment=None
    if request.method=='POST':
        #A commnet was created
        comment_form=CommentForm(data=request.POST)

        if comment_form.is_valid():
            #create comment object
            new_comment=comment_form.save(commit=False)
            #assign current post to comment
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments':comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form,
                   'similar_posts':similar_posts})


def post_search(request):
    form =SearchForm()
    query=None
    results=[]

    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results=Post.objects.annotate(search=SearchVector('title','body')).filter(search=query)
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})







def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            cd= form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated'\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


    else:
        form =LoginForm()
    return render(request,'blog/post/login.html',{'form':form})

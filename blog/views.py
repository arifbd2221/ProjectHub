from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django_filters.views import FilterView
from .filters import PostFilter
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comments, Images
from .CommentForm import AddCommentForm

from django.urls import reverse_lazy
from django.forms import modelformset_factory
from .forms import PostCreateForm

from django.core.paginator import Paginator
from datetime import datetime

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class FilteredPostList(FilterView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    filter_class = PostFilter
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'github_link', 'presentation_link', 'sellable', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def createpostform(request):
    imageset = modelformset_factory(Images, fields=('image',), extra=4)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = imageset(request.POST or None, request.FILES or None)

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()


            for f in formset:
                try:
                    photo = Images(post=post, image=f.cleaned_data['image'])
                    photo.save()
                    # return redirect('blog-home')
                except Exception as e:
                    break

            return redirect('blog-home')
    else:
        form = PostCreateForm()
        formset = imageset(queryset=Images.objects.none())

    context = {
        'form': form,
        'formset': formset
    }

    return render(request, 'blog/post_form.html', context)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'github_link', 'presentation_link', 'sellable', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})




def blogdetails(request, pk):
    post = get_object_or_404(Post, id=pk)
    owner = User.objects.get(username=post.author)
    comments = Comments.objects.filter(post=post).order_by('-id')
    if request.method == 'POST':
        commentForm = AddCommentForm(request.POST or None)

        if commentForm.is_valid():
            text = request.POST.get('text', None)
            if text is not None:
                comment = Comments(text=text, post=post, author=request.user)
                comment.save(force_insert=True)
                return HttpResponseRedirect(post.get_absolute_url())
    else:
        commentForm = AddCommentForm()
        
    context = {
        'post': post,
        'comments': comments,
        'commentForm': commentForm,
        'owner': owner,
    }

    return render(request, 'blog/post_detail_test.html', context)


class PostListViewByCategory(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        cat = self.kwargs.get('category')
        return Post.objects.filter(category__title=cat).order_by('-date_posted')


def addToCart(request, pk):
    print(type(pk))
    post = get_object_or_404(Post, id=pk)
    print(post.title)
    postkey = str(pk)
    request.session[postkey] = pk
    return render(request, 'blog/about.html', {})


def shoppingCart(request):
    cartdict = []
    totalcost = 0
    keys = list(request.session.keys())
    print(keys)
    
    for k in keys:
        print(type(k))
        try:
            pk = int(k)
            post = get_object_or_404(Post, id=pk)
            totalcost = totalcost + post.price
            cartdict.append(post)
        except ValueError:
            print('value error')


    return render(request, 'blog/shopping_cart.html', {'cartdict': cartdict, 'totalcost': int(totalcost),})


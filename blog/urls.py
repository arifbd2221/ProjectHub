from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostListViewByCategory
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', views.blogdetails, name='post-detail'),
    path('post/new/', views.createpostform, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<str:category>/', PostListViewByCategory.as_view(), name='post-category'),
    path('about/', views.about, name='blog-about'),
    path('cart/', views.shoppingCart, name='cart'),
    path('addtocart/<int:pk>/', views.addToCart, name='addtocart'),
]

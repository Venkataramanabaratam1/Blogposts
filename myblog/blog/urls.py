from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/edit/ajax/', views.post_edit_ajax, name='post_edit_ajax'),
    path('post/pin/', views.pin_post, name='pin_post'),  # URL for pinning a post
    path('post/unpin/', views.unpin_post, name='unpin_post'),  # URL for unpinning a post
    path('delete_post/', views.delete_post, name='delete_post'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.blog, name='blog'),  # Main blog page
]

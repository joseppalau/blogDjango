from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('drafts/', views.draft_post, name='post_draft'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.new_post, name='new_post'),
    path('post/<int:pk>/edit/', views.edit_post, name="edit_post"),
    path('post/<int:pk>/publish/', views.post_publish, name="post_publish"),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name="add_comment"),
    path('comment/<int:pk>/remove', views.remove_comment, name="remove_comment"),
]

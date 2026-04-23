from django.urls import path
from . import views

urlpatterns = [
    # PUBLIC
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('post/', views.post_public, name='post'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('qna/', views.qna_list, name='qna_list'),
    
    #CRUD QNA
    path('qna/add/', views.qna_create, name='qna_add'),
    path('qna/edit/<int:id>/', views.qna_update, name='qna_edit'),
    path('qna/delete/<int:id>/', views.qna_delete, name='qna_delete'),

    # AUTH
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('home-content/edit/', views.home_content_update, name='home_content_edit'),

    # CRUD

    # post
    path('posts/', views.post_list, name='post_list'),
    path('post/add/', views.post_create, name='post_add'),
    path('post/edit/<int:id>/', views.post_update, name='post_edit'),
    path('post/delete/<int:id>/', views.post_delete, name='post_delete'),
]

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('list/', views.post_list, name='post_list'),
    path('api/posts/', views.post_list_api, name='post_list_api'),
    path('write/', views.post_write, name='post_write'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    #path('delete/<int:post_id>/', views.delete_post, name='delete_post'), 삭제되었다는 페이지를 출력하는 대신, 게시글 목록으로 리다이렉트 되도록 수정했습니다.
   
    #path('movies/', views.movie_list, name='movie_list'), #영화 게시판 입니다.
    #path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('admin/', admin.site.urls), # 영화 데이터 받을 경로
    path('movies/', include('movies.urls')),# "

    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('boardlist/', views.boardlist, name='boardlist'),
    path('boardwrite/', views.boardwrite, name='boardwrite'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.signup, name='signup'),
    path('account/', include('account.urls')), 
    path('mypage/', views.mypage, name='mypage'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    #path('', include('movies.urls')),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),

]
# account/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from BoardProject.models import Post, Comment  # ✅ Post, Comment가 실제로 정의된 곳에서 가져오기
from BoardProject.forms import CommentForm

# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('home')  # 로그인 후 이동할 페이지
            except:
                return render(request, 'account/signup.html', {'error': 'Username already exists'})
        else:
            return render(request, 'account/signup.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'account/signup.html')


# 4번: 댓글 추가
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    return redirect('post_detail', post_id=post.id)


# 댓글 수정
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})


# 댓글 삭제
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', post_id=post_id)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.forms import SignUpForm
from .forms import CommentForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods


def boardlist(request):
    return render(request, 'boardlist.html')

def boardwrite(request):
    return render(request, 'boardwrite.html')

def main_page(request):
    return render(request, 'MainPage.html')

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-date')  # 글 전체를 날짜 내림차순으로 가져오기
    return render(request, 'BoardList.html', {'posts': posts})

def post_list_api(request):
    posts = Post.objects.all().order_by('-date')
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.title,
            'writer': post.writer.username if hasattr(post.writer, 'username') else str(post.writer),
            'date': post.date.strftime('%Y-%m-%d %H:%M') if post.date else ''
        })
    return JsonResponse(data, safe=False)

@login_required
def post_write(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        writer=request.user
        #writer = request.POST.get('writer')
        
        Post.objects.create(title=title, content=content, writer=writer)
        return redirect('post_list')  # 저장 후 목록 페이지로 이동
    return render(request, 'BoardWrite.html')

    from django.http import HttpResponseForbidden

#게시글 수정 추가
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.writer == request.user.username:  # 작성자 본인인지 확인 !=를 ==로 변경
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        post.title = title
        post.content = content
        post.save()
        
        return redirect('post_detail', post_id=post.id)
    
    return render(request, 'post_edit.html', {'post': post})

# #게시글 삭제 추가
# @login_required
# def delete_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)

#     if post.writer == request.user.username:  # 작성자 본인만 삭제 가능
#         return HttpResponseForbidden("삭제 권한이 없습니다.")

#     post.delete()
#     return redirect('post_list')

#게시글 삭제 수정 버전
@login_required
@require_http_methods(["POST"])  # DELETE 요청만 허용
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.writer != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    post.delete()
    return JsonResponse({'message': '삭제 성공'}, status=200)
    #여기까지

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()  # 댓글 작성 폼 생성
    return render(request, 'BoardDetail.html', {'post': post, 'form': form})

@login_required
def mypage(request):
    user = request.user  # 현재 로그인한 사용자
    return render(request, 'mypage.html', {'user': user})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 가입 후 로그인 페이지로
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # 로그인 성공하면 메인 페이지로
        else:
            messages.error(request, '아이디 또는 비밀번호가 틀렸습니다.')

    return render(request, 'registration/login.html')

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
    else:
        form = CommentForm()

    return render(request, 'BoardDetail.html', {'post': post, 'form': form})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment_edit.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # 작성자 본인만 삭제 가능
    if comment.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    post_id = comment.post.id
    comment.delete()
    return redirect('post_detail', post_id=post_id)
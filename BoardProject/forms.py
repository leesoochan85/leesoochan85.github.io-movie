from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from BoardProject.models import Comment,Post  # 현재 views.py와 같은 앱 디렉토리에 forms.py가 있어야 함
from .models import Comment, Post
from movies.models import Movie


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="이메일")
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': '아이디',
        }

    error_messages = {
        'password_mismatch': "비밀번호가 일치하지 않습니다.",
        'username_exists': "이미 사용 중인 아이디입니다.",
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'])
        return username


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '댓글을 입력하세요...',
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'movie']
        labels = {
            'title': '제목',
            'content': '내용',
            'movie': '영화 선택',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'movie': forms.Select(attrs={'class': 'form-control'}),
        }    
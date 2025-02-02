# registration/forms.py

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '用户名'}),
        }
        labels = {
            'username': '用户名',
        }
        help_texts = {
            'username': '',  # 移除帮助文本
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        if len(password1) < 8:
            raise forms.ValidationError("密码必须包含至少 8 个字符")
        # 添加更多自定义验证规则
        return password2

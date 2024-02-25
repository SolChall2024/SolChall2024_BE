from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Store, Menu, Option, Category, OptionContent


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='ID')  # ID가 맞음
    phone = forms.CharField(label='전화번호', max_length=20)
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    # 가게 이름을 저장할 추가적인 필드를 만듭니다.
    lastname = forms.CharField(label='가게 이름', max_length=150)

    class Meta(UserCreationForm.Meta):
        model = Store  # Store 모델로 변경
        fields = ['username', 'password1', 'password2', 'phone']  # 가게 이름 필드 제거

    def clean_username(self):
        id = self.cleaned_data['username']
        return id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_name = self.cleaned_data['lastname']  # 가게 이름을 last_name 필드에 저장
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    id = forms.CharField(label='ID')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class MenuForm(forms.ModelForm):
    new_category = forms.CharField(label='New Category', required=False)

    class Meta:
        model = Menu
        fields = ['name', 'price', 'menuImg']  # categoryId 필드 제거


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option', 'price', 'button']


class OptionContentForm(forms.ModelForm):
    class Meta:
        model = OptionContent
        fields = ['content', 'price', 'additional_field']  # 필드 목록에 새로운 필드 추가

    content = forms.CharField(label='Content', required=False)  # content 필드를 선택적 필드로 변경
    additional_field = forms.CharField(label='Additional Field', required=False)  # 추가 필드 추가
import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User, UserProfile
from re import findall


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

    # def clean_email(self):
    #     data = self.cleaned_data["email"]
    #     if User.objects.get(email=data):
    #         raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован!")
    #     return data


class UserProfileForm(UserChangeForm):

    image = forms.ImageField(widget=forms.FileInput(), required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'first_name', 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    # def clean_age(self):
    #     data = self.cleaned_data["age"]
    #     if data < 18:
    #         raise forms.ValidationError("Только для пользователей старше 18 лет. Спасибо за понимание.")
    #     return data
    #

    # def clean_image(self):
    #     data = self.cleaned_data['image']
    #     if data.size > 1024:
    #         raise forms.ValidationError('Файл слишком большой')
    #     return data


    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if findall(r'^[^@]+@[^@.]+\.[^@]+$', data) == []:
    #         raise forms.ValidationError('Адрес электронной почты введён некорректно')
    #     return data


    # def clean_first_name(self):
    #     data = self.cleaned_data['first_name']
    #     if not data.istitle():
    #         raise forms.ValidationError('Имя должно начинаться с заглавной буквы')
    #     return data
    #
    #
    # def clean_last_name(self):
    #     data = self.cleaned_data['last_name']
    #     if not data.istitle():
    #         raise forms.ValidationError('Фамилия должна начинаться с заглавной буквы')
    #     return data


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'about_me', 'gender', 'langs')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'

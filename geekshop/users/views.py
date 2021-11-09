from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView

from geekshop.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from mainapp.models import Product
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from baskets.models import Basket
from users.models import User

# Create your views here.


class LoginListView(LoginView, BaseClassContextMixin):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Geekshop - Авторизация'
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        sup = super(LoginListView, self).get(request, *args, **kwargs)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        return sup


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'title': 'Geekshop - Авторизация',
#                'form': form
#                }
#     return render(request, 'users/login.html', context)

class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = 'Geekshop - Регистрация'

    def post (self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request, 'Вы успешно зарегистрировались! Пройдите верификацию email!')
            # form.save()
            # messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect (self.success_url)
        else:
            messages.error(request, 'Вы не зарегистрировались! Проверьте введённые данные, в первую очередь адрес электронной почты.')
        return redirect (reverse_lazy('users:register'))

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} \n перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    @staticmethod
    def verify(request, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_created = None
                user.is_active = True
                user.save()
                auth.login(request, user)
            return render(request, 'users/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

# def register (request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {'title': 'Geekshop - Регистрация',
#                'form': form
#                }
#     return render(request, 'users/register.html', context)


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop - Профайл'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    # @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    # def dispatch(self, request, *args, **kwargs):
    #     return super(ProfileFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile),
        return context

    def post (self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        form_edit = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and form_edit.is_valid():
            form.save()
            return redirect (self.success_url)
        return redirect (self.success_url)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно отредактировали Профиль!')
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#     context = {
#         'title': 'Geekshop - Профайл',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#         'total_quantity': sum(basket.quantity for basket in baskets),
#         'total_sum': sum(basket.sum() for basket in baskets),
#
#     }
#     return render(request, 'users/profile.html', context)


class Logout(LogoutView):
    template_name = 'mainapp/index.html'


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

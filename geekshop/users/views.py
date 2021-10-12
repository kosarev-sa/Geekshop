from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView

from geekshop.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from baskets.models import Basket
from users.models import User

# Create your views here.


class LoginListView(LoginView, BaseClassContextMixin):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Geekshop - Авторизация'

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
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect (self.success_url)
        return redirect (self.success_url)

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
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def post (self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
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

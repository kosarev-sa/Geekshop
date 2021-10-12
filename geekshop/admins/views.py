from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductCategoryAdminRegisterForm, \
    ProductAdminRegisterForm
from geekshop.mixin import CustomDispatchMixin, BaseClassContextMixin
from mainapp.models import ProductCategory, Product
from users.models import User


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'


class UserCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    form_class = UserAdminRegisterForm
    template_name = 'admins/admin-users-create.html'
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создание пользователя'


class UserUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    form_class = UserAdminProfileForm
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Обновление пользователя'


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active == True:
            self.object.is_active = False
        else:
            self.object.is_active = True

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    title = 'Админка | Категории товаров'


class ProductCategoryCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    form_class = ProductCategoryAdminRegisterForm
    template_name = 'admins/admin-category-create.html'
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админка | Создание категории товаров'


class ProductCategoryUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    form_class = ProductCategoryAdminRegisterForm
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админка | Обновление категории товаров'


class ProductCategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active == True:
            self.object.is_active = False
        else:
            self.object.is_active = True

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    title = 'Админка | Товары'


class ProductCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    form_class = ProductAdminRegisterForm
    template_name = 'admins/admin-product-create.html'
    success_url = reverse_lazy('admins:admin_products')
    title = 'Админка | Создание товара'


class ProductUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    form_class = ProductAdminRegisterForm
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:admin_products')
    title = 'Админка | Обновление товара'


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active == True:
            self.object.is_active = False
        else:
            self.object.is_active = True

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

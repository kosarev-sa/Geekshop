from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from geekshop.mixin import UserDispatchMixin, BaseClassContextMixin
from mainapp.models import Product
from baskets.models import Basket

# Create your views here.


@login_required
def basket_add(request, product_id):
    user_select = request.user
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user_select, product=product)
    if not baskets.exists():
        Basket.objects.create(user=user_select, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, product_id):
    Basket.objects.get(id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets,
            'total_quantity': sum(basket.quantity for basket in baskets),
            'total_sum': sum(basket.sum() for basket in baskets),
        }
        result = render_to_string('baskets/baskets.html', context)
        return JsonResponse({'result': result})


# class BasketCreateView(CreateView, UserDispatchMixin, BaseClassContextMixin):
#     model = Basket
#     fields = ['product']
#     template_name = 'mainapp/products.html'
#     success_url = reverse_lazy('products:index')
#     title = 'Админка | Создание товара'
#
#     def post(self, request, *args, **kwargs):
#         if 'product_id' in kwargs:
#             product_id = kwargs['product_id']
#             if 'product_id':
#                 product = Product.objects.get(id=product_id)
#                 baskets = Basket.objects.filter(user=request.user, product=product)
#                 if not baskets.exists():
#                     Basket.objects.create(user=request.user, product=product, quantity=1)
#                 else:
#                     basket = baskets.first()
#                     basket.quantity += 1
#                     basket.save()
#         return redirect(self.success_url)


# class BasketDeleteView(DeleteView, UserDispatchMixin):
#     model = Basket
#     template_name = 'users/profile.html'
#     success_url = reverse_lazy('users:profile')


# class BasketUpdateView(UpdateView, UserDispatchMixin, BaseClassContextMixin):
#     model = Basket
#     fields = ['product']
#     pk_url_kwarg = 'basket_id '
#     template_name = 'users/profile.html'
#     success_url = reverse_lazy('users:profile')

    # def get_context_data(self, **kwargs):
    #     context = super(BasketUpdateView, self).get_context_data(**kwargs)
    #     context.update({
    #         'baskets': Basket.objects.filter(user=self.request.user),
    #         'total_quantity': sum(basket.quantity for basket in Basket.objects.filter(user=self.request.user)),
    #         'total_sum': sum(basket.sum() for basket in Basket.objects.filter(user=self.request.user)),
    #         })
    #     return context
    #
    # def get(self, request, *args, **kwargs):
    #     super(BasketUpdateView, self).get(request, *args, **kwargs)
    #     if request.is_ajax():
    #         basket_id = kwargs[self.pk_url_kwarg]
    #         quantity = kwargs['quantity']
    #         baskets = Basket.objects.filter(id=basket_id)
    #         if baskets.exists():
    #             basket = baskets.first()
    #             if quantity > 0:
    #                 basket.quantity = quantity
    #                 basket.save()
    #             else:
    #                 basket.delete()
    #
    #         result = render_to_string('baskets/baskets.html', self.get_context_data(**kwargs), request=request)
    #         return JsonResponse({'result': result})
    #     return redirect(self.success_url)

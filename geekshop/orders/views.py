from pprint import pprint

from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from orders.forms import OrderItemForm, OrderForm
from orders.models import Order, OrderItem


class OrderList(ListView, BaseClassContextMixin, UserDispatchMixin):
    model = Order
    title = 'Список заказов'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):

    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate,self).get_context_data(**kwargs)
        context['title'] = 'Geekshop | Создать заказа'

        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormset(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormset()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormset()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderCreate,self).form_valid(form)


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop | Просмотр заказа'


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop | Обновление заказа'

        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormset(self.request.POST, instance=self.object)
        else:
            formset = OrderFormset(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            for item in self.object.get_items():
                if item.quantity == 0:
                    item.delete()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


class OrderUpdateStatus(UpdateView, BaseClassContextMixin):
    model = Order
    template_name = 'orders/order_form_change_status.html'
    title = 'Обновление статуса заказа'
    fields = ['status']
    success_url = reverse_lazy('orders:list')

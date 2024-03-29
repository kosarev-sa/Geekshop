from django.core.management import BaseCommand
from django.db.models import F, When, Case, DecimalField, IntegerField, Q
from datetime import timedelta

from prettytable import PrettyTable

from orders.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_3__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)

        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)

        action_3__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_3__order = When(action_3__condition, then=ACTION_3)

        action_1__price = When(action_1__condition, then=F('product__price') * F('quantity') * action_1__discount)
        action_2__price = When(action_2__condition, then=F('product__price') * F('quantity') * -action_2__discount)
        action_3__price = When(action_3__condition, then=F('product__price') * F('quantity') * action_3__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_3__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_3__price,
                output_field=DecimalField(),

            )).order_by('action_order', 'total_price').select_related()

        t_list = PrettyTable(['Заказ', 'Товар', 'Скидка', 'Время'])
        t_list.align = 'l'
        for orderitem in test_orders:
            t_list.add_row([f'{orderitem.action_order} заказ №{orderitem.pk}', f'{orderitem.product.name:15}',
                            f'{abs(orderitem.total_price):6.2f} руб.',
                            orderitem.order.updated - orderitem.order.created])
        print(t_list)

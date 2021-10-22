from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOISES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отмена заказа')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(max_length=3, verbose_name='статус', choices=ORDER_STATUS_CHOISES, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __str__(self):
        return f'Текущий заказ №{self.pk}'

    def get_items(self):
        return self.orderitems.select_related()

    def get_total_quantity(self):
        return sum(list(map(lambda item: item.quantity, self.get_items())))

    def get_total_cost(self):
        return sum(list(map(lambda item: item.get_product_cost(), self.get_items())))

#     def get_summary(self):
#         items = self.get_items
#         return {
#             'total_quantity': sum(list(map(lambda item: item.quantity, items))),
#             'total_cost': sum(list(map(lambda item: item.get_product_cost, items)))
#         }
#
    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.status = self.CANCEL
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

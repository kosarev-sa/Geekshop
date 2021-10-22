from django.urls import path

from orders.views import OrderList, OrderCreate, OrderUpdate, OrderDetail, OrderDelete, order_forming_complete, \
    OrderUpdateStatus

app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('confirm/<int:pk>/', order_forming_complete, name='forming_complete'),
    path('update_status/<int:pk>/', OrderUpdateStatus.as_view(), name='update_status'),

    ]

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import json
# import os.path
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from geekshop.mixin import BaseClassContextMixin
from mainapp.models import Product, ProductCategory


# Create your views here.


class IndexView(TemplateView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = 'GeekShop'                  # или extra_context = {'title': 'GeekShop'}


# def index(request):
#     return render(request, 'mainapp/index.html')


class ProductListView(ListView, BaseClassContextMixin):
    model = Product
    template_name = 'mainapp/products.html'
    paginate_by = 3
    title = 'Geekshop - Каталог'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update({
            'categories': ProductCategory.objects.all(),
            })
        return context


class ProductCategoryView(ProductListView):

    def get_queryset(self, *args, **kwargs):
        products = Product.objects.filter(category_id=self.kwargs['category_id']) \
            if self.kwargs['category_id'] else Product.objects.all()
        return products


# def products(request, category_id=None, page_id=1):
#     ## with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'db.json'), "r", encoding='UTF-8') as f:
#     ##     content = json.load(f)
#     products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
# 
#     paginator = Paginator(products, 3)                  # 3 - количесвто товаров на странице
#     try:
#         products_paginator = paginator.page(page_id)    # список товаров на странице page_id
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)          # отобразим первую страницу
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages())      # отобразим все товары
# 
#     context = {
#         'title': 'geekshop',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all(),
#         ## 'products': content,
#         #             [{'link': 'img class=card-img-top src=/static/vendor/img/products/Adidas-hoodie.png alt=',
#         #               'name': 'Худи черного цвета с монограммами adidas Originals',
#         #               'price': '6 090,00',
#         #               'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
#         #
#         #              {'link': 'img class=card-img-top src=/static/vendor/img/products/Blue-jacket-The-North-Face.png '
#         #                       'alt=',
#         #               'name': 'Синяя куртка The North Face',
#         #               'price': '23 725,00',
#         #               'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'},
#         #
#         #              {'link': 'img class=card-img-top '
#         #                       'src=/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png alt=>',
#         #               'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
#         #               'price': '3 390,00',
#         #               'description': 'Материал с плюшевой текстурой. Удобный и мягкий.'},
#         #
#         #              {'link': 'img class=card-img-top src=/static/vendor/img/products/Black-Nike-Heritage-backpack.png '
#         #                       'alt=>',
#         #               'name': 'Черный рюкзак Nike Heritage',
#         #               'price': '2 340,00',
#         #               'description': 'Плотная ткань. Легкий материал.'},
#         #
#         #              {'link': 'img class=card-img-top src=/static/vendor/img/products/Black-Dr-Martens-shoes.png alt=>',
#         #               'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
#         #               'price': '13 590,00',
#         #               'description': 'Гладкий кожаный верх. Натуральный материал.'},
#         #
#         #              {'link': 'img class=card-img-top '
#         #                       'src=/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png alt=>',
#         #               'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
#         #               'price': '2 890,00',
#         #               'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.'},
#         # ]
#     }
#     return render(request, 'mainapp/products.html', context)

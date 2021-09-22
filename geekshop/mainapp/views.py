from django.shortcuts import render

# import json
# import os.path

from mainapp.models import Product, ProductCategory

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    ## with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'db.json'), "r", encoding='UTF-8') as f:
    ##     content = json.load(f)
    context = {
        'title': 'geekshop',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
        ## 'products': content,
        #             [{'link': 'img class=card-img-top src=/static/vendor/img/products/Adidas-hoodie.png alt=',
        #               'name': 'Худи черного цвета с монограммами adidas Originals',
        #               'price': '6 090,00',
        #               'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
        #
        #              {'link': 'img class=card-img-top src=/static/vendor/img/products/Blue-jacket-The-North-Face.png '
        #                       'alt=',
        #               'name': 'Синяя куртка The North Face',
        #               'price': '23 725,00',
        #               'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'},
        #
        #              {'link': 'img class=card-img-top '
        #                       'src=/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png alt=>',
        #               'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
        #               'price': '3 390,00',
        #               'description': 'Материал с плюшевой текстурой. Удобный и мягкий.'},
        #
        #              {'link': 'img class=card-img-top src=/static/vendor/img/products/Black-Nike-Heritage-backpack.png '
        #                       'alt=>',
        #               'name': 'Черный рюкзак Nike Heritage',
        #               'price': '2 340,00',
        #               'description': 'Плотная ткань. Легкий материал.'},
        #
        #              {'link': 'img class=card-img-top src=/static/vendor/img/products/Black-Dr-Martens-shoes.png alt=>',
        #               'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
        #               'price': '13 590,00',
        #               'description': 'Гладкий кожаный верх. Натуральный материал.'},
        #
        #              {'link': 'img class=card-img-top '
        #                       'src=/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png alt=>',
        #               'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
        #               'price': '2 890,00',
        #               'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.'},
        # ]
    }
    return render(request, 'mainapp/products.html', context)

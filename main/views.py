from django.shortcuts import render, redirect

from .models import *
from .forms import *

def index(request):
    cat_list = CategoryByUrl.objects.all()

    products_by_category = {
        category: ProductsSortedByRating.objects.filter(cat_url=category.url)[:12] for category in cat_list
    }
    print(products_by_category)
    data = {
        'title': 'Main page',
        'products_by_category': products_by_category,
    }
    return render(request, 'main/index.html', context=data)


def products_in_category(request, cat_url):
    category = CategoryByUrl.objects.get(url=cat_url)
    products = ProductsSortedByRating.objects.filter(cat_url=category.url)[:40]
    return render(request, 'main/category.html', context={'title': category.name, 'category': category, 'products': products})


def product_info(request, cat_url, product_url):
    product = ProductByUrl.objects.get(cat_url=cat_url, url=product_url)
    category = CategoryByUrl.objects.get(url=cat_url)
    return render(request, 'main/product.html', context={'title': product.title, 'category': category, 'product': product})


def create_category(request):
    error = ''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_category')
        else:
            error = 'Неверно заполенные данные'
    cat_list = CategoryByUrl.objects.all()
    form = CategoryForm()
    return render(request, 'main/create_category.html', context={'cat_list': cat_list, 'form': form, 'error': error})


def about(request):
    return render(request, 'main/about.html')
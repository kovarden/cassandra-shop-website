from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView
import hashlib

from .models import *
from .forms import *


def login(request, user):
    if user is not None:
        request.session['user_id'] = str(user.id)
        request.session['hash'] = user.password
    return request

def login_view(request):
    error = ''
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                request.session['user_id'] = str(user.id)
                request.session['hash'] = user.password
                request.session.modified = True
                print(request.session.items())
            return render(request, 'main/signin.html', context={'form': form, 'error': error})
        else:
            error = 'Incorrectly filled data'
    form = SignInForm()
    return render(request, 'main/signin.html', context={'form': form, 'error': error})
    #
    # error = ''
    # if request.method == 'POST':
    #     form = AuthorizationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('index')
    #     else:
    #         error = 'Неверно заполенные данные'
    # cat_list = CategoryByUrl.objects.all()
    # form = CategoryForm()
    # return render(request, 'main/create_category.html', context={'cat_list': cat_list, 'form': form, 'error': error})
    return render(request, '')


def index(request):
    cat_list = CategoryByUrl.objects.all()

    products_by_category = {
        category: ProductsSortedByRating.objects.filter(cat_url=category.url)[:12] for category in cat_list
    }
    data = {
        'title': 'Main page',
        'products_by_category': products_by_category,
    }
    return render(request, 'main/index.html', context=data)


class ProductCategoryMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ProductCategoryMixin, self).get_context_data(**kwargs)
        context['category'] = CategoryByUrl.objects.get(url=self.kwargs['cat_url'])
        return context


class ProductDetailsByCategory(ProductCategoryMixin, ListView):
    model = ProductsSortedByRating
    template_name = 'main/category.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductsSortedByRating.objects.filter(cat_url=self.kwargs['cat_url'])


class ProductDetailView(ProductCategoryMixin, DetailView):
    model = ProductByUrl
    template_name = 'main/product.html'
    context_object_name = 'product'

    def get_object(self):
        return ProductByUrl.objects.get(cat_url=self.kwargs['cat_url'], url=self.kwargs['product_url'])


def create_category(request):
    error = ''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            category = form.save()
            return redirect(reverse('category', kwargs={'cat_url': category.url}))
        else:
            error = 'Incorrectly filled data'
    form = CategoryForm()
    return render(request, 'main/create_category.html', context={'form': form, 'error': error})


class CategoryUpdateView(UpdateView):
    model = CategoryByUrl
    form_class = CategoryForm
    template_name = 'main/create_category.html'
    context_object_name = 'category'

    def get_object(self):
        return CategoryByUrl.objects.get(url=self.kwargs['cat_url'])


class CategoryDeleteView(DeleteView):
    model = CategoryByUrl
    success_url = '/'
    template_name = 'main/delete_category.html'
    context_object_name = 'category'

    def get_object(self):
        return CategoryByUrl.objects.get(url=self.kwargs['cat_url'])


def create_product(request, cat_url):
    error = ''
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.id = uuid.uuid1()
            product.cat_url = CategoryByUrl.objects.get(url=cat_url).url
            product.save()
            return redirect(reverse('product-detail', kwargs={'cat_url': cat_url, 'product_url': product.url}))
        else:
            error = 'Incorrectly filled data'
    category = CategoryByUrl.objects.get(url=cat_url)
    form = ProductForm()
    return render(request, 'main/create_product.html', context={'category': category, 'form': form, 'error': error})


def about(request):
    return render(request, 'main/about.html')

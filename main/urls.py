from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('login', views.login_view),
    path('create_category', views.create_category, name='create-category'),
    path('<str:cat_url>/update', views.CategoryUpdateView.as_view(), name='update-category'),
    path('<str:cat_url>/delete', views.CategoryDeleteView.as_view(), name='delete-category'),
    path('<str:cat_url>', views.ProductDetailsByCategory.as_view(), name='category'),
    path('<str:cat_url>/create', views.create_product, name='create-product'),
    path('<str:cat_url>/<str:product_url>', views.ProductDetailView.as_view(), name='product-detail'),
]

from django.forms import ModelForm, TextInput

from .models import CategoryByUrl, ProductByUrl, Products, ProductsSortedByRating


class CategoryForm(ModelForm):
    class Meta:
        model = CategoryByUrl
        fields = ['name', 'url']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category url'
            })
        }


# class ProductForm(ModelForm):
#     class Meta:
#         model = Products
#         fields = ['name', 'url']
#         widgets = {
#             'name': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter category name'
#             }),
#             'url': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter category url'
#             })
#         }
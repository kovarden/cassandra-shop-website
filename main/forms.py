from django.forms import ModelForm, TextInput, Form, NumberInput, Textarea
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


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


class ProductForm(ModelForm):
    class Meta:
        model = ProductByUrl
        fields = ['title', 'url', 'price', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
            }),
            'url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product url'
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description'
            })
        }


class AuthorizationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
        if user.username.startswith('b'):
            raise ValidationError(
                _("Sorry, accounts starting with 'b' aren't welcome here."),
                code='no_b_users',
            )

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
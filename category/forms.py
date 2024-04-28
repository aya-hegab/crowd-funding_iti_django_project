from django import forms
from django.core.exceptions import ValidationError
from category.models import *

class CategoryForm(forms.ModelForm):
  class Meta:
    model=Category
    fields=['name']
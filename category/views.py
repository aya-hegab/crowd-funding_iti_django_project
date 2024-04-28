from .models import *
from .forms import *
from django.views.generic import UpdateView, DeleteView, ListView, CreateView
from django.urls import reverse_lazy


class updateCategory(UpdateView):
  model = Category
  template_name= 'category/updateCategory.html'
  form_class=CategoryForm
  context_object_name='form'
  success_url=reverse_lazy("category.list")

class addCategory(CreateView):
  model = Category
  template_name= 'category/addCategory.html'
  form_class=CategoryForm
  context_object_name='form'
  success_url=reverse_lazy("category.list")


class listCategory(ListView):
  model = Category
  template_name= 'category/index.html'
  context_object_name='category'

class deleteCategory(DeleteView):
  model = Category
  template_name= 'category/deleteCategory.html'
  context_object_name='category'
  success_url=reverse_lazy("category.list")


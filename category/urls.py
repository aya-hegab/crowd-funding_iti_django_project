from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', staff_member_required(views.listCategory.as_view()), name="category.list"),
    path('add', staff_member_required(views.addCategory.as_view()), name="category.add"),
    path('delete/<pk>', staff_member_required(views.deleteCategory.as_view()), name='category.delete'),
    path('update/<pk>', staff_member_required(views.updateCategory.as_view()), name='category.update'),
    
]
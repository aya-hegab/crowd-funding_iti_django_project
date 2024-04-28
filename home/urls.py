from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path("category/<int:id>/", views.Cate, name='cate'),
    path("search/", views.Search.as_view(), name='search'),
]

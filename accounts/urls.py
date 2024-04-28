from django.urls import path,include
from . import views
from .views import *
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static



urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('profile/',views.myProfile,name='myProfile'),
    # path('Register/',RegistrationForm.as_view(),name='RegistrationForm'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('Delete/<int:user_id>/',views.DeleteAccount,name='DeleteAccount'),
    path('delete_confirmation/<int:user_id>/', views.delete_confirmation, name='delete_confirmation'),
    path('update/<int:user_id>/', views.updateUser, name='update_user'),
    # path('edit/<int:user_id>/', views.edit_profile, name='edit'),
    path('info/', views.additional_info, name='additional_info'),
    path('userImage/', views.userImage, name='userImage'),
    path('accounts/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    
]
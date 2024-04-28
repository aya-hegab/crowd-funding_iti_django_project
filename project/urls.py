from django.contrib import admin
from django.urls import path,include
from . import views
from .views import *


urlpatterns = [
    
    path('list',views.projectslist,name='projects.list'),
    path('<int:proid>',views.projectdetailes,name="project.detailes"),
    path('create',views.createproject,name="project.create"),
    path('report/<int:proid>', views.report_project, name='projects.report'),
    path('thank-you-for-reporting/', views.thank_you_for_reporting, name='thank_you_for_reporting'),
    path('reportcomment/<int:comment_id>', views.report_comment, name='report_comment'),
    path('rate_project/<int:project_id>', views.rate_project, name='rate_project'),
    path('project/<int:project_id>/cancel/', views.cancel_project, name='cancel_project'),
    path('userprofile/', views.user_projects, name='user_project'),
    path("tag/<slug:slug>/", views.Tagging, name='tagged'),
    
]

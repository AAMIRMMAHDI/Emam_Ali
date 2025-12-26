from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('list/', views.list_view, name='list_view'),
    path('about/', views.about_view, name='about_view'),
    path('tips/<slug:slug>/', views.article_detail, name='article_detail'),
]
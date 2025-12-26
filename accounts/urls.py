# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='accounts/logged_out.html',  # صفحه بعد از خروج
        next_page='accounts:login'  # بعد از خروج بره به لاگین
    ), name='logout'),
    path('', views.ExamView.as_view(), name='exam_page'),
    path('submit/', views.SubmitExamView.as_view(), name='submit_exam'),
]
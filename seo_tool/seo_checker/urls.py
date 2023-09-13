from django.urls import path
from . import views

urlpatterns = [
    path('', views.seo_checker, name='seo_checker'),
]

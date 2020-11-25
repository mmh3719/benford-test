from django.urls import path

from benford import views

urlpatterns = [
    path('', views.index, name='index'),
]

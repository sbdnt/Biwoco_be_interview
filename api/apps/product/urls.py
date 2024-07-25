from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCreateProductView.as_view()),
    path("<int:pk>/", views.UpdateDeletProductView.as_view()),
]
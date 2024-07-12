from django.urls import path
from .views import ProductListView, ProductView

urlpatterns = [
    path("products", ProductListView.as_view()),
    path("products/<int:pk>", ProductView.as_view()),
]

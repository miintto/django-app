from django.urls import path

from .views import OrderSearchView, OrderView

urlpatterns = [
    path("orders", OrderView.as_view()),
    path("orders/<int:pk>", OrderSearchView.as_view()),
]

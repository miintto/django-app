from rest_framework.generics import ListAPIView, RetrieveAPIView

from .mixins import ProductListMixin, ProductMixin
from .serializers import ProductDetailSerializer, ProductSerializer


class ProductListView(ProductListMixin, ListAPIView):
    serializer_class = ProductSerializer


class ProductView(ProductMixin, RetrieveAPIView):
    serializer_class = ProductDetailSerializer

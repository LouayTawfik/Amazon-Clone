from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter
from .pagination import MyPagination
from .serializers import ProductListSerializer, ProductDetailSerializer, BrandListSerializer, BrandDetailSerializer
from .models import Brand, Product

# @api_view(['GET'])
# def product_list_api(request):
#     products = Product.objects.all()[:20]  # list
#     data = ProductSerializer(products, many=True, context={'request': request}).data  # json
#     return Response({'products': data})

# @api_view(['GET'])
# def product_detail_api(request, product_id):
#     products = Product.objects.get(id=product_id)
#     data = ProductSerializer(products, context={'request': request}).data  # json
#     return Response({'product': data})

class ProductListAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all().select_related('brand').prefetch_related('review_product')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['flag', 'brand', 'price']
    search_fields = ['name', 'subtitle', 'description']
    ordering_fields = ['price', 'quantity']
    filterset_class = ProductFilter
    pagination_class = MyPagination

    # def get_queryset(self):
    #     return super().get_queryset().select_related('brand').prefetch_related('review_product')


class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('review_product')


class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer


class BrandDetailAPI(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
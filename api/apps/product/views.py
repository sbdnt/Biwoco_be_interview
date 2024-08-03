from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ListCreateProductView(ListCreateAPIView):
    model = Product
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new Product successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Product unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeletProductView(RetrieveUpdateDestroyAPIView):
    model = Product
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update Product successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Update Product unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        product.delete()

        return JsonResponse({
            'message': 'Delete Car successful!'
        }, status=status.HTTP_200_OK)

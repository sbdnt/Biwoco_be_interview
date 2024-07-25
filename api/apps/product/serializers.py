from rest_framework import serializers

from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('sku', 'barcode', 'title', 'description', 'unit_cost', 'quantity', 'min_quantity')
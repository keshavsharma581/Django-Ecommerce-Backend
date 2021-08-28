from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_null=True, allow_empty_file=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',
                  'stock', 'image', 'category')

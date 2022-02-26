from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class StockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            stock_product = StockProduct(product=position.get('product'), quantity=position.get('quantity'), price=position.get('price'), stock=stock)
            stock_product.save()
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        instance.positions.filter().delete()
        for position in positions:
            StockProduct.objects.update_or_create(product=position.get('product'), quantity=position.get('quantity'), price=position.get('price'), stock_id=instance.id)
        return stock

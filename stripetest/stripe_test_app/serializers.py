from rest_framework import serializers
from .models import Order, Item, OrderItem

class ItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['title', 'description', 'price']

    def get_price(self, obj: Item):
        return obj.price / 100
    
class ItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['title', 'description', 'price']

class OrderItemDetailSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]
        read_only_fields = fields

class OrderItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]
        
        
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, source="orderitem_set")
    
    class Meta:
        model = Order
        fields = ["paid", "items"]
        read_only_fields = fields

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, source="orderitem_set")

    class Meta:
        model = Order
        fields = ["items"]
        
    def create(self, validated_data):
        items = validated_data.pop("orderitem_set")
        order = Order.objects.create(**validated_data)
        
        for item in items:
            OrderItem.objects.create(order=order, **item)
            
        return order

from rest_framework import serializers
from .models import Customer, Order

class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField()  # Store FK as ID
    product_name = serializers.CharField(max_length=100)
    order_date = serializers.DateField()

    def create(self, validated_data):
        customer = Customer.objects.get(pk=validated_data["customer_id"])
        return Order.objects.create(customer=customer, **validated_data)

    def update(self, instance, validated_data):
        if "customer_id" in validated_data:
            instance.customer = Customer.objects.get(pk=validated_data["customer_id"])
        instance.product_name = validated_data.get("product_name", instance.product_name)
        instance.order_date = validated_data.get("order_date", instance.order_date)
        instance.save()
        return instance

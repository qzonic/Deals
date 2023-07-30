from django.db.models import Sum, Q
from django.db.transaction import atomic
from rest_framework import serializers

from .models import Customer, Deal, Gem


class GemSerializer(serializers.ModelSerializer):
    """ Serializer for gem model """

    class Meta:
        model = Gem
        fields = (
            'name',
        )


class CustomerSerializer(serializers.ModelSerializer):
    """ Serializer for customer model """

    spent_money = serializers.DecimalField(max_digits=9, decimal_places=2)
    gems = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'username',
            'spent_money',
            'gems'
        )

    def get_gems(self, obj):
        customers = Customer.objects.annotate(
            spent_money=Sum('deals__total')
        ).order_by('-spent_money')[:5]
        gems_list = []
        for customer in customers:
            gems_list += [gem for gem in customer.gems.all()]
        gems = []
        for gem in obj.gems.all():
            if gems_list.count(gem) >= 2:
                gems.append(gem)
        return GemSerializer(gems, many=True).data


class DealSerializer(serializers.ModelSerializer):
    """ Serializer for deal model """

    customer = serializers.CharField(
        max_length=64
    )
    item = serializers.CharField(
        max_length=64
    )

    class Meta:
        model = Deal
        fields = (
            'customer',
            'item',
            'total',
            'quantity',
            'date'
        )
        required_fields = fields

    @atomic
    def create(self, validated_data):
        customer_username = validated_data.get('customer')
        gem_name = validated_data.get('item')
        customer, customer_created = Customer.objects.get_or_create(
            username=customer_username
        )
        gem, gem_created = Gem.objects.get_or_create(name=gem_name)
        if (customer_created or gem_created) and gem not in customer.gems.all():
            customer.gems.add(gem)
        validated_data['customer'] = customer
        validated_data['item'] = gem
        return super().create(validated_data)

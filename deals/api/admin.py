from django.db.models import Sum
from django.contrib import admin

from .models import Gem, Customer, Deal


class GemAdmin(admin.ModelAdmin):
    """ Gem admin model """

    list_display = (
        'name',
        'get_deals_count',
    )
    search_fields = (
        'name',
    )

    @admin.display(description='In deals count', empty_value='-')
    def get_deals_count(self, obj):
        return int(obj.deals.count())


class CustomerAdmin(admin.ModelAdmin):
    """ Gem admin model """

    list_display = (
        'username',
        'get_deals_count',
        'get_spent_money'
    )
    search_fields = (
        'username',
    )

    @admin.display(description='Deals count', empty_value='-')
    def get_deals_count(self, obj):
        return int(obj.deals.count())

    @admin.display(description='Spent money', empty_value='-')
    def get_spent_money(self, obj):
        return obj.deals.aggregate(spent_money=Sum('total'))['spent_money']


class DealAdmin(admin.ModelAdmin):
    """ Deal admin model """

    list_display = (
        'customer',
        'item',
        'quantity',
        'total',
        'date'
    )
    list_filter = (
        'date',
    )


admin.site.register(Gem, GemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Deal, DealAdmin)

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'status', 'display_total_price', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'full_name', 'phone_number')

    inlines = (OrderItemInline,)

    date_hierarchy = 'created_at'

    def display_total_price(self, obj):
        return f"{obj.get_total_price:,} so'm"

    display_total_price.short_description = "Umumiy summa"

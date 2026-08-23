from django.contrib import admin
from .models import Kategoriya, MashinaModeli, Mahsulot, MahsulotRasmi

class MahsulotRasmiInline(admin.TabularInline):
    model = MahsulotRasmi
    extra = 2

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'artikul_raqami', 'kategoriya', 'narxi', 'ombordagi_soni', 'faol','rasm')
    list_filter = ('faol', 'kategoriya')
    search_fields = ('nomi', 'artikul_raqami')
    inlines = [MahsulotRasmiInline]

admin.site.register(Kategoriya)
admin.site.register(MashinaModeli)

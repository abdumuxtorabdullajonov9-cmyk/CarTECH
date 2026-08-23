from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Mahsulot

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('delivered', 'Yetkazib berildi'),
        ('cancelled', 'Bekor qilindi'),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Buyurtmachi",
    )
    full_name = models.CharField(max_length=100, verbose_name="F.I.SH")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    shipping_address = models.TextField(verbose_name="Yetkazib berish manzili")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Buyurtma holati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma vaqti")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.full_name}"

    @property
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Buyurtma"
    )
    product = models.ForeignKey(
        Mahsulot,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Mahsulot"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (sotib olingan paytdagi)")

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

    def __str__(self):
        if self.product:
            return f"{self.product.nomi} ({self.quantity} ta)"
        return f"O'chirilgan mahsulot ({self.quantity} ta)"

    def get_cost(self):
        return self.price * self.quantity

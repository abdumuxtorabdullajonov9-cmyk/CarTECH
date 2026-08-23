from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=20,unique=True,blank=True,null=True,verbose_name="Telefon nomer")
    email = models.EmailField(unique=True,verbose_name="Elektron pochta")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.username} ({self.email})"

class Profile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User"
    )

    shipping_address = models.TextField(blank=True,null=True,verbose_name="Yetkazib berish manzili")
    city = models.CharField(max_length=100,blank=True,null=True,verbose_name="Shahar/Tuman")
    birth_date = models.DateField(blank=True,null=True,verbose_name="Tug'ulgan kuningiz")
    avatar = models.ImageField(upload_to='avatars/',blank=True,null=True,verbose_name="Profil rasmi")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"Profil: {self.user.username} "






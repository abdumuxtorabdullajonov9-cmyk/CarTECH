from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil ma\'lumotlari'
    fields = ('city', 'birth_date', 'avatar')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = (ProfileInline,)

    list_display = ['username', 'email', 'phone_number', 'is_staff']

    search_fields = ('username', 'email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy malumotlar', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Huquqlar', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Sanalar', {'fields': ('last_login', 'date_joined')}),
    )

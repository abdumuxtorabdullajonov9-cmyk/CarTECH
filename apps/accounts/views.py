from django.shortcuts import render, redirect
from django.contrib.auth import login
from django import forms
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Foydalanuvchi nomi'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Elektron pochta'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Telefon raqam'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parol'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

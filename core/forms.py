from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Форма для контактного сообщения"""
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'})
    )
    subject = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема сообщения'})
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше сообщение', 'rows': 5})
    )
    
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message') 
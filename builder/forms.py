from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Build, CPU, GPU, Motherboard, RAM, PSU, Case


class BuildForm(forms.ModelForm):
    """Форма создания/редактирования сборки"""
    
    class Meta:
        model = Build
        fields = ['name', 'description', 'cpu', 'gpu', 'motherboard', 'ram', 'psu', 'case', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название сборки'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание (опционально)'
            }),
            'cpu': forms.Select(attrs={'class': 'form-select'}),
            'gpu': forms.Select(attrs={'class': 'form-select'}),
            'motherboard': forms.Select(attrs={'class': 'form-select'}),
            'ram': forms.Select(attrs={'class': 'form-select'}),
            'psu': forms.Select(attrs={'class': 'form-select'}),
            'case': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gpu'].required = False
        self.fields['case'].required = False
        self.fields['description'].required = False
        
        # Пустые варианты
        self.fields['cpu'].empty_label = '— Выберите процессор —'
        self.fields['gpu'].empty_label = '— Выберите видеокарту (опционально) —'
        self.fields['motherboard'].empty_label = '— Выберите материнскую плату —'
        self.fields['ram'].empty_label = '— Выберите RAM —'
        self.fields['psu'].empty_label = '— Выберите блок питания —'
        self.fields['case'].empty_label = '— Выберите корпус (опционально) —'


class CPUFilterForm(forms.Form):
    """Форма фильтрации процессоров"""
    socket = forms.ChoiceField(
        required=False,
        choices=[('', 'Все сокеты')] + list(CPU.SOCKET_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Мин. цена'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Макс. цена'})
    )


class GPUFilterForm(forms.Form):
    """Форма фильтрации видеокарт"""
    vram = forms.ChoiceField(
        required=False,
        choices=[('', 'Любой объём'), ('4', '4 GB'), ('6', '6 GB'), ('8', '8 GB'), ('12', '12 GB')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Мин. цена'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Макс. цена'})
    )


class RegistrationForm(UserCreationForm):
    """Форма регистрации"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтвердите пароль'})
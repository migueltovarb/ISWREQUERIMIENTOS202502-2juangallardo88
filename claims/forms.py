from django import forms
from .models import Claim, FAQ
import uuid
import re

class ClaimForm(forms.ModelForm):
    contact_info = forms.CharField(
        max_length=200,
        label="Correo o Teléfono",
        help_text="Ingresa tu correo electrónico o número de teléfono"
    )

    class Meta:
        model = Claim
        fields = [
            'full_name', 'order_number',
            'description', 'evidence', 'priority', 'zone'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe tu problema en detalle'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'order_number': forms.TextInput(attrs={'placeholder': 'Número de pedido (opcional)'}),
            'zone': forms.TextInput(attrs={'placeholder': 'Barrio o zona'}),
            'priority': forms.RadioSelect(),
            'evidence': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        contact_info = cleaned_data.get('contact_info')
        description = cleaned_data.get('description')
        zone = cleaned_data.get('zone')

        # Validaciones RF19
        if not full_name or len(full_name.strip()) < 3:
            raise forms.ValidationError("El nombre completo debe tener al menos 3 caracteres.")
        
        if not description or len(description.strip()) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        
        if not zone or len(zone.strip()) < 2:
            raise forms.ValidationError("Debes especificar una zona o barrio.")
        
        if not contact_info:
            raise forms.ValidationError("Debes proporcionar un correo electrónico o teléfono.")

        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        
        # Generar número único RF20
        if not instance.number:
            instance.number = 'R-' + uuid.uuid4().hex[:8].upper()
        
        # Separar email y teléfono
        contact_info = self.cleaned_data.get('contact_info', '')
        if self._is_email(contact_info):
            instance.email = contact_info
            instance.phone = ''
        else:
            instance.phone = contact_info
            instance.email = ''
        
        instance.contact = contact_info
        
        # RF2: Asociar automáticamente si el usuario está autenticado
        if user and user.is_authenticated:
            instance.created_by = user
        
        if commit:
            instance.save()
        return instance
    
    @staticmethod
    def _is_email(value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, value) is not None


class ClaimSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por número de reclamo o número de pedido',
            'class': 'form-control'
        })
    )


class ClaimFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'Todos los estados')] + list(Claim.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'Todas las prioridades')] + list(Claim.PRIORITY_CHOICES)

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Estado")
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label="Prioridad")
    zone = forms.CharField(max_length=100, required=False, label="Zona", widget=forms.TextInput(attrs={'placeholder': 'Filtrar por zona'}))
    date_from = forms.DateField(required=False, label="Desde", widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, label="Hasta", widget=forms.DateInput(attrs={'type': 'date'}))


class ClaimUpdateForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['status', 'assigned_to', 'priority']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.RadioSelect(),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

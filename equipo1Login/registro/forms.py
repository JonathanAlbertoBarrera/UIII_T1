from django import forms
from django.core.exceptions import ValidationError
import re
from core.models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'apellidos', 'edad', 'email', 'mensaje']


    def clean_nombre(self):
        data = self.cleaned_data['nombre']
        pattern = r'^[A-Za-zÁÉÍÓÚÑáéíóúñ ]{10,}$'
        if not re.fullmatch(pattern, data):
            raise ValidationError(
                'El nombre debe contener solo letras y espacios (mínimo 10 caracteres).'
            )
        return data

    def clean_matricula(self):
        data = self.cleaned_data['matricula']
        pattern = r'^[0-9]{5}[A-Za-z]{2}[0-9]{3}$'
        if not re.fullmatch(pattern, data):
            raise ValidationError(
                'La matrícula debe tener 5 números, 2 letras y 3 números.'
            )
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        pattern = r'^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$'
        if not re.fullmatch(pattern, data):
            raise ValidationError(
                'El correo debe pertenecer al dominio utez.edu.mx.'
            )
        return data

    def clean_telefono(self):
        data = self.cleaned_data['telefono']
        pattern = r'^\d{10}$'
        if not re.fullmatch(pattern, data):
            raise ValidationError(
                'El teléfono debe contener exactamente 10 dígitos.'
            )
        return data

    def clean_rfc(self):
        data = self.cleaned_data['rfc'].upper()
        pattern = r'^[A-Z]{4}[0-9]{6}[A-Z0-9]{3}$'
        if not re.fullmatch(pattern, data):
            raise ValidationError(
                'RFC inválido. Usa mayúsculas: 4 letras, 6 números y 3 alfanuméricos.'
            )
        return data

    def clean_contrasena(self):
        data = self.cleaned_data['contrasena']
        pattern = r'^(?=.*\d)(?=.*[A-Z])(?=.*[!#$%&?]).{8,}$'
        if not re.fullmatch(pattern, data):
            raise ValidationError(
                'La contraseña no cumple con los requisitos de seguridad.'
            )
        return data

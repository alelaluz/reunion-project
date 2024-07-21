from django import forms
from django.forms import ValidationError
from django.core.validators import EmailValidator
import re


def solo_caracteres(value_campoNombre):
    if any(char.isdigit() for char in value_campoNombre):
        raise ValidationError('el nombre no puede contener numeros. %(valor)s',
                              code='Invalid',
                              params={'valor': value_campoNombre})


def custom_validate_email(value_campoEmail):

    email_regex = r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'
    if not re.match(email_regex, value_campoEmail.lower()):
        raise ValidationError('el email no es valido')


class ContactoForm(forms.Form):

    nombre = forms.CharField(
        label="Nombre",
        max_length=30,
        validators=(solo_caracteres,),
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'solo letras'}
        )
    )

    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        validators=(custom_validate_email,),
        error_messages={
            'required': 'por favor completa este campo'
        },
        # widget=forms.EmailInput(
        # attrs={'class': 'form-control', 'type': 'email'})
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'email'})
    )

    asunto = forms.CharField(
        label="Asunto",
        max_length=100,
        validators=(solo_caracteres,),
        widget=forms.TextInput(
            attrs={'class': 'form-control', }
        )

    )

    mensaje = forms.CharField(
        label="Mensaje",
        max_length=500,
        widget=forms.Textarea(
            attrs={'rows': 5, 'class': 'form-control'}
        )

    )

    # si la tupla la ubico abajo de la tipo_consulta  arroja error
    TIPO_CONSULTA = (
        ('', 'seleccione-'),
        (1, 'Inscripciones'),
        (2, 'soporte'),
        (3, 'instructor/a'),


    )

    tipo_consulta = forms.ChoiceField(
        label='tipo de consulta',
        choices=TIPO_CONSULTA,
        widget=forms.Select(attrs={'class': 'form-control'}))

    suscripcion = forms.BooleanField(
        label='deseo subscribirme a las novedades de grupete   ',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'value': 1}
        )
    )

    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 10:
            raise ValidationError(
                "debes especificar mejor el mensaje que nos envias ")
        return data

    # si quiere suscripbirse y es MARIANO no le damos la suscripcion
    # valida datos en conjunto , no esta asociado a un campo especifijo
    # mi_formulario.non_field_error todos los errores que no son de ningun campo, aca
    # va a estar el error de no aceptamos marianos
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        suscripcion = cleaned_data.get('suscripcion')

        if suscripcion and nombre and ("MARIANO" in nombre.upper()):
            msg = " no le bindamos info a Marianos"
            self.add_error('nombre', msg)
            raise ValidationError(msg)

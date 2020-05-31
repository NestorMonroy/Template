from django import forms


class SimpleCaptchaField(forms.CharField):

    def __init__(self, label='Confirmación de persona', **kwargs):
        super().__init__(label=label, required=True, **kwargs)
        self.widget.attrs['placeholder'] = 'Por favor escriba "gracias" en ingles'

    def clean(self, value):
        value = super().clean(value)
        if value == 'Thank you':
            return value
        else:
            raise forms.ValidationError('La respuesta es diferente!')

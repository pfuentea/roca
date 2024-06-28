from ..models import  ResumenCotizacion
from django import forms

class ResumenCotizacionForm(forms.ModelForm):
    class Meta:
        model = ResumenCotizacion
        fields = []
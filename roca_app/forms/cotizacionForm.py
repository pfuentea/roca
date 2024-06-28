from django import forms
from ..models import DetalleCotizacion

class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = [ 'diametro', 'ancho', 'alto', 'costo_instalacion_motor', 'costo_instalacion_roller', 'costo_instalacion_cenefa', 'cantidad']

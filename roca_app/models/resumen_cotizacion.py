from django.db import models
from .cliente import Cliente  # Importa el modelo Cliente
from django.contrib.auth.models import User

class ResumenCotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    usuario_generador = models.ForeignKey(User, on_delete=models.CASCADE)
    cotizacion_id=models.CharField(max_length=50,default='')

    def __str__(self):
        return f"Resumen de Cotización para {self.cliente.nombre} - {self.fecha}"
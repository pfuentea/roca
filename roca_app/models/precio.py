from django.db import models
from .roller import Roller  # Importar el modelo Roller desde el mismo paquete

class Precio(models.Model):
    roller = models.ForeignKey(Roller, on_delete=models.CASCADE, related_name='precios')
    ancho_inicial = models.DecimalField(max_digits=6, decimal_places=2)
    ancho_final = models.DecimalField(max_digits=6, decimal_places=2)
    alto_inicial = models.DecimalField(max_digits=6, decimal_places=2)
    alto_final = models.DecimalField(max_digits=6, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Precio de {self.roller.nombre}: ${self.precio}"
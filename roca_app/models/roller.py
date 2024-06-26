from django.db import models
from .diametro import Diametro  # Importar el modelo Diametro desde el mismo paquete

class Roller(models.Model):
    nombre = models.CharField(max_length=100)
    diametro = models.ForeignKey(Diametro, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
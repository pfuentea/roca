from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    documento = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
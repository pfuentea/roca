from django.db import models

class Diametro(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion
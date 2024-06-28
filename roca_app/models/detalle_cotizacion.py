from django.db import models
from .cliente import Cliente  # Importa el modelo Cliente
from .roller import Roller  # Importa el modelo Roller y otros modelos necesarios
from .diametro import Diametro
from .motor import Motor
from .gateway import Gateway
from .cenefa import Cenefa
from .control import Control
from .resumen_cotizacion import ResumenCotizacion  # Importa el modelo ResumenCotizacion


class DetalleCotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    roller = models.ForeignKey(Roller, on_delete=models.CASCADE)
    diametro = models.ForeignKey(Diametro, on_delete=models.SET_NULL, null=True, blank=True)
    ancho = models.DecimalField(max_digits=10, decimal_places=2)
    alto = models.DecimalField(max_digits=10, decimal_places=2)
    motor = models.ForeignKey(Motor, on_delete=models.SET_NULL, null=True, blank=True)
    control = models.ForeignKey(Control, on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.ForeignKey(Gateway, on_delete=models.SET_NULL, null=True, blank=True)
    cenefa = models.ForeignKey(Cenefa, on_delete=models.SET_NULL, null=True, blank=True)
    costo_instalacion_motor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_instalacion_roller = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_instalacion_cenefa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    resumen_cotizacion = models.ForeignKey(ResumenCotizacion, on_delete=models.CASCADE, default=1)  # Clave foránea
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)  # Nuevo campo total

    def __str__(self):
        return f"Detalle de Cotización para {self.cliente.nombre} - {self.roller.nombre}"
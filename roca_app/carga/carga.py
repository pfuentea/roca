import openpyxl
from django.db import transaction

from roca_app.models.roller import Roller
from roca_app.models.precio import Precio

# Ruta del archivo Excel
ruta_archivo = 'data_precios.xlsx' 

# Abrir el archivo Excel
wb = openpyxl.load_workbook(ruta_archivo)
hoja = wb['Hoja1']  # Suponiendo que la data está en la hoja 'Hoja1'

# Leer los anchos iniciales
anchos_iniciales = [
    float(celda.value) for celda in hoja['C6'][1:]  # Ignorar la cabecera
]

# Leer los anchos finales
anchos_finales = [
    float(celda.value) for celda in hoja['C7'][1:]  # Ignorar la cabecera
]

# Leer los precios
precios = []
for fila in hoja.iter_rows(min_row=9):  # Iniciar desde la fila 9 (incluyendo la cabecera)
    fila_precios = []
    for celda in fila[2:]:  # Columnas C:9 en adelante (precios)
        fila_precios.append(float(celda.value))
    precios.append(fila_precios)

# Procesar y guardar la data en el modelo Django

roller= Roller.objects.get(id=5)
with transaction.atomic():  # Asegurar atomicidad de la transacción
    for i, (ancho_inicial, ancho_final, precio_fila) in enumerate(zip(anchos_iniciales, anchos_finales, precios)):
        # Buscar o crear el roller (asumiendo que el nombre del roller está en la fila 8, columna A)

        # Recorrer los precios por fila y crear instancias de Precio
        for alto_inicial, alto_final, precio in zip(hoja['A{}'.format(10 + i)], hoja['B{}'.format(10 + i)], precio_fila):
            precio_obj = Precio.objects.create(
                roller=roller,
                ancho_inicial=ancho_inicial,
                ancho_final=ancho_final,
                alto_inicial=alto_inicial,
                alto_final=alto_final,
                precio=precio
            )

            # Guardar el precio
            precio_obj.save()
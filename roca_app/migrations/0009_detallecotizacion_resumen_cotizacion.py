# Generated by Django 4.2.7 on 2024-06-27 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roca_app', '0008_resumencotizacion_detallecotizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallecotizacion',
            name='resumen_cotizacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='roca_app.resumencotizacion'),
        ),
    ]

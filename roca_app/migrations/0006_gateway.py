# Generated by Django 4.2.7 on 2024-06-26 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roca_app', '0005_control'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]

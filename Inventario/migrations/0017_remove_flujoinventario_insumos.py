# Generated by Django 5.0.1 on 2024-03-19 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0016_detalleflujoinventario_cantidad_insumo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flujoinventario',
            name='insumos',
        ),
    ]

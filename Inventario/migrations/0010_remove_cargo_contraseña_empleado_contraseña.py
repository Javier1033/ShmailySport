# Generated by Django 5.0.1 on 2024-03-12 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0009_arl_activo_cargo_activo_ciudad_activo_eps_activo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='contraseña',
        ),
        migrations.AddField(
            model_name='empleado',
            name='contraseña',
            field=models.CharField(default='', max_length=30),
        ),
    ]

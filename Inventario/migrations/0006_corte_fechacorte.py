# Generated by Django 5.0.1 on 2024-02-27 17:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0005_flujoinventario_flujoproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='corte',
            name='fechaCorte',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

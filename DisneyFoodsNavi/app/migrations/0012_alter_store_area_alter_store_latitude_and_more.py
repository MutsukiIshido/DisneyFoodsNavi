# Generated by Django 5.1 on 2025-02-19 02:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_food_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='app.area'),
        ),
        migrations.AlterField(
            model_name='store',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)]),
        ),
        migrations.AlterField(
            model_name='store',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)]),
        ),
        migrations.AlterUniqueTogether(
            name='foodstore',
            unique_together={('food', 'store')},
        ),
    ]

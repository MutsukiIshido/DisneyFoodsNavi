# Generated by Django 5.1 on 2025-01-27 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

# Generated by Django 5.1 on 2025-01-20 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_reviewimages_review_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewimages',
            name='review_image_path',
            field=models.ImageField(blank=True, null=True, upload_to='review_images'),
        ),
    ]

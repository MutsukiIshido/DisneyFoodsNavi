# Generated by Django 5.1 on 2025-01-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_reviewimages_review_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewimages',
            name='review_image_path',
            field=models.ImageField(blank=True, null=True, upload_to='review_images/'),
        ),
    ]

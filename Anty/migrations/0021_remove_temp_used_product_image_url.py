# Generated by Django 3.2.6 on 2021-10-05 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0020_alter_gender_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temp_used_product',
            name='image_url',
        ),
    ]

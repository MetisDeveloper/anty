# Generated by Django 3.2.6 on 2021-10-23 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0031_alter_used_product_image_temp_used_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='used_product_image',
            old_name='temp_used_product',
            new_name='used_product',
        ),
    ]
# Generated by Django 3.2.6 on 2021-10-20 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0028_used_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='used_product_image',
            name='temp_used_product',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='Anty.temp_used_product'),
            preserve_default=False,
        ),
    ]

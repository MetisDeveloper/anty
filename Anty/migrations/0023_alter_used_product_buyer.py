# Generated by Django 3.2.6 on 2021-10-06 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0022_alter_temp_used_product_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='used_product',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_user', to=settings.AUTH_USER_MODEL),
        ),
    ]

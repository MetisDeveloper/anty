# Generated by Django 3.2.6 on 2021-10-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0018_brand_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image_url',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
# Generated by Django 3.2.6 on 2021-09-25 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0009_address_tel'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='firstname',
            field=models.TextField(default=0, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='firstnmae_furi',
            field=models.TextField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lastname',
            field=models.TextField(default=0, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='lastname_furi',
            field=models.TextField(max_length=20, null=True),
        ),
    ]
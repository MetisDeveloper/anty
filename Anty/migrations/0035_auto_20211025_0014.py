# Generated by Django 3.2.6 on 2021-10-24 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0034_remove_address_primary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='portalcode',
            new_name='postalcode',
        ),
        migrations.AddField(
            model_name='address',
            name='detail4',
            field=models.TextField(max_length=30, null=True),
        ),
    ]

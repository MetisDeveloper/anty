# Generated by Django 3.2.6 on 2021-10-23 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0033_user_stripe_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='primary',
        ),
    ]
# Generated by Django 3.2.6 on 2021-10-25 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0035_auto_20211025_0014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='detail4',
        ),
        migrations.AddField(
            model_name='address',
            name='kana1',
            field=models.TextField(default='カナ', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='kana2',
            field=models.TextField(default='カナ', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='kana3',
            field=models.TextField(max_length=30, null=True),
        ),
    ]
# Generated by Django 3.2.6 on 2021-09-25 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anty', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='ゲスト', max_length=32, null=True, verbose_name='username'),
        ),
    ]

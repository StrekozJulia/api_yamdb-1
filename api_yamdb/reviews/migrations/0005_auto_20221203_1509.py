# Generated by Django 2.2.16 on 2022-12-03 12:09

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20221203_1224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_name_owner'),
        ),
    ]

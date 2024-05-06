# Generated by Django 5.0.3 on 2024-04-11 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shophubapp', '0002_rename_consoles_console'),
    ]

    operations = [
        migrations.AlterField(
            model_name='console',
            name='cat',
            field=models.IntegerField(choices=[(1, 'PlayStation'), (2, 'Xbox'), (3, 'Nintendo Switch'), (4, 'PS4')], verbose_name='Product Category'),
        ),
    ]

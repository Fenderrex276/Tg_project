# Generated by Django 4.1.5 on 2023-01-24 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_alter_periodictask_fun'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodictask',
            name='is_change',
            field=models.BooleanField(default=False, verbose_name='Поменялось ли'),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-13 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_alter_periodictask_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timezone',
            field=models.CharField(default=0, max_length=7, verbose_name='Таймзона'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='number_dispute',
            field=models.CharField(max_length=6, verbose_name='уникальный идентификатор диспута'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0015_alter_disputeadmin_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='disputeadmin',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен ли администратор?'),
        ),
    ]
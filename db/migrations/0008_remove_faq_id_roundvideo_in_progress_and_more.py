# Generated by Django 4.1.2 on 2022-11-18 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_faq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='id',
        ),
        migrations.AddField(
            model_name='roundvideo',
            name='in_progress',
            field=models.CharField(choices=[('done', 'Done'), ('waiting', 'Waiting')], default='waiting', max_length=15, verbose_name='На рассмотрении'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='chat_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='faq',
            name='faq_num',
            field=models.IntegerField(default=0),
        ),
    ]
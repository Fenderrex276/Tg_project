# Generated by Django 4.1.2 on 2022-11-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_roundvideo_n_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('number_dispute', models.CharField(max_length=6)),
                ('chat_id', models.IntegerField()),
                ('problem', models.CharField(max_length=256)),
                ('solved', models.CharField(choices=[('new', 'New'), ('done', 'Done'), ('in_process', 'In Process')], max_length=10, verbose_name='статус вопроса')),
            ],
        ),
        migrations.DeleteModel(
            name='FAQ',
        ),
        migrations.RemoveField(
            model_name='support',
            name='id_dispute',
        ),
        migrations.AddField(
            model_name='support',
            name='number_dispute',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
    ]
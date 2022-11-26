# Generated by Django 4.1.3 on 2022-11-26 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoundVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.CharField(max_length=90)),
                ('user_tg_id', models.IntegerField()),
                ('chat_tg_id', models.IntegerField()),
                ('code_in_video', models.CharField(max_length=4)),
                ('status', models.CharField(choices=[('good', 'Good'), ('bad', 'Bad'), ('other', 'Other')], max_length=20, verbose_name='Статус кружочка')),
                ('id_video', models.IntegerField()),
                ('type_video', models.CharField(choices=[('test', 'Test'), ('dispute', 'Dispute'), ('archive', 'Archive')], default='none', max_length=20, verbose_name='Тип видео')),
                ('n_day', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('number_dispute', models.CharField(max_length=6)),
                ('chat_id', models.IntegerField()),
                ('problem', models.CharField(max_length=256)),
                ('solved', models.CharField(choices=[('new', 'New'), ('done', 'Done'), ('in_process', 'In Process')], max_length=10, verbose_name='статус вопроса')),
            ],
        ),
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
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='ID пользователя в Телеграмм')),
                ('user_name', models.CharField(max_length=20, verbose_name='Имя пользователя')),
                ('action', models.CharField(max_length=20, verbose_name='?')),
                ('additional_action', models.CharField(max_length=20, verbose_name='?')),
                ('start_disput', models.CharField(max_length=10, verbose_name='Когда начинается диспут')),
                ('deposit', models.IntegerField(verbose_name='Сумма депозита')),
                ('promocode_user', models.CharField(max_length=10, verbose_name='Промокод пользователя')),
                ('promocode_from_friend', models.CharField(max_length=10, verbose_name='Промокод-приглашение')),
                ('count_days', models.IntegerField(verbose_name='Сколько дней длится диспут')),
                ('number_dispute', models.CharField(max_length=6, verbose_name='?')),
            ],
        ),
    ]

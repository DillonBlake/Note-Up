# Generated by Django 4.0.1 on 2022-02-12 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_settings_user_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_log',
            name='logs',
        ),
        migrations.AddField(
            model_name='user_log',
            name='ip',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='user_log',
            name='url',
            field=models.CharField(default='', max_length=250),
        ),
    ]

# Generated by Django 4.0 on 2022-01-22 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebook',
            name='group',
            field=models.CharField(default='Old', max_length=250),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-11 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='text',
        ),
        migrations.AddField(
            model_name='result',
            name='label_group',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='result',
            name='word',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]

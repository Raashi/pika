# Generated by Django 2.2.3 on 2020-02-24 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20200220_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Job name'),
        ),
    ]
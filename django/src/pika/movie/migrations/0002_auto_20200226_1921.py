# Generated by Django 2.2.3 on 2020-02-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='overview',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Overview'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True, verbose_name='Popularity'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rus_overview',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Overview in russian'),
        ),
    ]

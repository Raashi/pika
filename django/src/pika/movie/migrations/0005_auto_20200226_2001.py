# Generated by Django 2.2.3 on 2020-02-26 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_moviereleasedate_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='overview',
            field=models.CharField(blank=True, max_length=2048, null=True, verbose_name='Overview'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rus_overview',
            field=models.CharField(blank=True, max_length=2048, null=True, verbose_name='Overview in russian'),
        ),
    ]
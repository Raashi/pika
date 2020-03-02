# Generated by Django 2.2.3 on 2020-02-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20200226_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='biography',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='person',
            name='known_for_department',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Known for department'),
        ),
        migrations.AlterField(
            model_name='person',
            name='popularity',
            field=models.DecimalField(decimal_places=3, default='0.00', max_digits=6, verbose_name='Popularity'),
        ),
        migrations.AlterField(
            model_name='person',
            name='rus_biography',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Russian biography'),
        ),
    ]
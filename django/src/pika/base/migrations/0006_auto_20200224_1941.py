# Generated by Django 2.2.3 on 2020-02-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20200224_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Collection name'),
        ),
    ]
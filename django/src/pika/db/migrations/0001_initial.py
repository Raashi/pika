# Generated by Django 2.2.3 on 2020-02-17 10:16

from django.db import migrations, models
import pika.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', pika.db.fields.ISOField(max_length=2, primary_key=True, serialize=False, verbose_name='ISO country code')),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Country name')),
                ('rus_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Country name in russian')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', pika.db.fields.ISOField(max_length=2, primary_key=True, serialize=False, verbose_name='ISO code')),
                ('name', models.CharField(max_length=32, verbose_name='Language name')),
                ('rus_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Language name in russian')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'db_table': 'lang',
            },
        ),
    ]
# Generated by Django 2.2.3 on 2020-02-26 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20200226_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereleasedate',
            name='note',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Release note'),
        ),
    ]
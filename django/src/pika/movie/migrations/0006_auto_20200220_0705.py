# Generated by Django 2.2.3 on 2020-02-20 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20200220_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieparticipant',
            name='tmdb_cast_id',
        ),
        migrations.AddField(
            model_name='movieparticipant',
            name='tmdb_credit_id',
            field=models.CharField(default='', max_length=32, verbose_name='TMDB credit ID'),
            preserve_default=False,
        ),
    ]
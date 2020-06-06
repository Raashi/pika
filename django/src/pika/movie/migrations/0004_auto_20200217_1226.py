# Generated by Django 2.2.3 on 2020-02-17 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20200217_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieparticipant',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='movie.Movie', verbose_name='Movie'),
        ),
    ]
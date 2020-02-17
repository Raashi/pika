# Generated by Django 2.2.3 on 2020-02-17 10:16

from django.db import migrations, models
import django.db.models.deletion
import pika.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', pika.db.fields.TMDBId(primary_key=True, serialize=False, verbose_name='TMDB Id')),
                ('imdb_id', pika.db.fields.IMDBId(blank=True, db_index=True, max_length=9, null=True, unique=True, verbose_name='IMDB Id')),
                ('name', models.CharField(max_length=64, verbose_name='Person name')),
                ('rus_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Person name in russian')),
                ('gender', pika.db.fields.GenderField(blank=True, choices=[(0, 'unknown'), (1, 'Female'), (2, 'Male')], default=0, null=True, verbose_name='Gender')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
                ('deathday', models.DateField(blank=True, null=True, verbose_name='Death day')),
                ('known_for_department', models.CharField(blank=True, choices=[('Lighting', 'Lighting'), ('Crew', 'Crew'), ('Sound', 'Sound'), ('Actors', 'Actors'), ('Directing', 'Directing'), ('Visual Effects', 'Visual Effects'), ('Writing', 'Writing'), ('Camera', 'Camera'), ('Costume & Make-Up', 'Costume & Make-Up'), ('Editing', 'Editing'), ('Art', 'Art'), ('Production', 'Production')], max_length=20, null=True, verbose_name='Known for department')),
                ('biography', models.CharField(blank=True, max_length=256, null=True, verbose_name='Biography')),
                ('rus_biography', models.CharField(blank=True, max_length=256, null=True, verbose_name='Russian biography')),
                ('popularity', models.DecimalField(decimal_places=2, default='0.00', max_digits=6, verbose_name='Popularity')),
                ('profile', pika.db.fields.ProfileImageField(blank=True, max_length=64, null=True, verbose_name='Profile')),
                ('adult', models.BooleanField(default=False, verbose_name='Adult')),
                ('homepage', models.URLField(blank=True, null=True, verbose_name='Homepage')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='PersonTMDBImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='Path')),
                ('aspect_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Aspect ratio')),
                ('width', models.IntegerField(default=-1, verbose_name='Width')),
                ('height', models.IntegerField(default=-1, verbose_name='Height')),
                ('vote_average', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Vote average')),
                ('vote_count', models.IntegerField(default=0, verbose_name='Vote count')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='person.Person', verbose_name='Person')),
            ],
            options={
                'verbose_name': 'Person image',
                'verbose_name_plural': 'Person images',
                'db_table': 'person_image',
            },
        ),
    ]

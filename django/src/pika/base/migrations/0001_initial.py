# Generated by Django 2.2.3 on 2020-02-17 10:16

from django.db import migrations, models
import django.db.models.deletion
import pika.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', pika.db.fields.TMDBId(primary_key=True, serialize=False, verbose_name='TMDB Id')),
                ('name', models.CharField(max_length=64, verbose_name='Collection name')),
                ('rus_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Collection name in russian')),
                ('poster', pika.db.fields.PosterImageField(blank=True, max_length=64, null=True, verbose_name='Poster')),
                ('backdrop', pika.db.fields.BackdropImageField(blank=True, max_length=64, null=True, verbose_name='Backdrop')),
                ('overview', models.CharField(blank=True, max_length=256, null=True, verbose_name='Overview')),
                ('rus_overview', models.CharField(blank=True, max_length=256, null=True, verbose_name='Overview in russian')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
                'db_table': 'collection',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', pika.db.fields.TMDBId(primary_key=True, serialize=False, verbose_name='TMDB Id')),
                ('name', models.CharField(max_length=32, verbose_name='Genre name')),
                ('rus_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='Genre name in russian')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': 'genre',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('Lighting', 'Lighting'), ('Crew', 'Crew'), ('Sound', 'Sound'), ('Actors', 'Actors'), ('Directing', 'Directing'), ('Visual Effects', 'Visual Effects'), ('Writing', 'Writing'), ('Camera', 'Camera'), ('Costume & Make-Up', 'Costume & Make-Up'), ('Editing', 'Editing'), ('Art', 'Art'), ('Production', 'Production')], max_length=20, verbose_name='Department name')),
                ('name', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='Job name')),
                ('rus_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Job name in russian')),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', pika.db.fields.TMDBId(primary_key=True, serialize=False, verbose_name='TMDB Id')),
                ('name', models.CharField(max_length=64, verbose_name='Keyword')),
            ],
            options={
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
                'db_table': 'keyword',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', pika.db.fields.TMDBId(primary_key=True, serialize=False, verbose_name='TMDB Id')),
                ('name', models.CharField(max_length=128, verbose_name='Company name')),
                ('rus_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Company name in russian')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Company description')),
                ('rus_description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Company description in russian')),
                ('headquarters', models.CharField(blank=True, max_length=256, null=True, verbose_name='Headquarters')),
                ('homepage', models.URLField(blank=True, null=True, verbose_name='Homepage')),
                ('logo', pika.db.fields.LogoImageField(blank=True, max_length=64, null=True, verbose_name='Company logo')),
                ('origin_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to='db.Country', verbose_name='Origin country')),
                ('parent_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Company', verbose_name='Parent company')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'db_table': 'company',
            },
        ),
    ]

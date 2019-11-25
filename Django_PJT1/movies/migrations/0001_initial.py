# Generated by Django 2.2.7 on 2019-11-25 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MovieCd', models.IntegerField()),
                ('movieName', models.CharField(max_length=30)),
                ('movieNameE', models.CharField(max_length=30)),
                ('pubDate', models.IntegerField()),
                ('runtime', models.CharField(max_length=200)),
                ('director', models.CharField(max_length=200)),
                ('userRating', models.FloatField()),
                ('poster_url', models.CharField(max_length=140)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie_has_genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
    ]

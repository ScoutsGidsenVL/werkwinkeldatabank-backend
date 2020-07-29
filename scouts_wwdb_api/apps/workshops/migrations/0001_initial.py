# Generated by Django 3.0.8 on 2020-07-29 12:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('necessities', models.TextField()),
                ('theme', models.ManyToManyField(to='workshops.Theme')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

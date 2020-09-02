# Generated by Django 3.1 on 2020-09-02 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0007_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingblockinstance',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='workshops.category'),
        ),
        migrations.AddField(
            model_name='buildingblockinstance',
            name='short_description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='buildingblocktemplate',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='workshops.category'),
        ),
        migrations.AddField(
            model_name='buildingblocktemplate',
            name='short_description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='workshop',
            name='is_sensitive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
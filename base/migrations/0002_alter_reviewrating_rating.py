# Generated by Django 4.0.5 on 2022-06-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='rating',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
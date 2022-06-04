# Generated by Django 4.0.2 on 2022-06-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.PositiveSmallIntegerField(choices=[(1, 'English'), (2, 'French'), (3, 'German'), (4, 'Portugese')], default=1, null=True),
        ),
    ]

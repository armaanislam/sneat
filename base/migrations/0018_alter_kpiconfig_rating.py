# Generated by Django 4.0.5 on 2022-06-07 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_employee_kpiobjective_project_sbu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpiconfig',
            name='rating',
            field=models.CharField(blank=True, choices=[('1. Exceeded.', '1. Exceeded.'), ('2. Achieved all aspects.', '2. Achieved all aspects.'), ('3. Achieved the essnential requirements.', '3. Achieved the essnential requirements.'), ('4. Did not achieve.', '4. Did not achieve.')], default='', max_length=255),
        ),
    ]
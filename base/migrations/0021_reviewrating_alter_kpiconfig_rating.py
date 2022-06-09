# Generated by Django 4.0.5 on 2022-06-07 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_subsbu_employee_basic_salary_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(blank=True, choices=[('1. Exceeded.', '1. Exceeded.'), ('2. Achieved all aspects.', '2. Achieved all aspects.'), ('3. Achieved the essnential requirements.', '3. Achieved the essnential requirements.'), ('4. Did not achieve.', '4. Did not achieve.')], default='', max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='kpiconfig',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kpi_review_rating', to='base.reviewrating'),
        ),
    ]
# Generated by Django 4.0.5 on 2022-06-09 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_employee_sbu_alter_employee_sub_sbu_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('Software Architect', 'Software Architect'), ('QA Engineer', 'QA Engineer'), ('Sr. Implementation Engineer, AML', 'Sr. Implementation Engineer, AML'), ('Project Manager', 'Project Manager'), ('Senior Project Manager & Enterprise Architect', 'Senior Project Manager & Enterprise Architect')], default='', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(to='base.role'),
        ),
    ]
# Generated by Django 4.2.7 on 2023-12-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_course_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]

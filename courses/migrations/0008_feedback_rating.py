# Generated by Django 4.2.7 on 2023-11-28 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_course_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]

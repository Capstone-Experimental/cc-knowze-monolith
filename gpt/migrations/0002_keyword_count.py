# Generated by Django 4.2.7 on 2023-11-05 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

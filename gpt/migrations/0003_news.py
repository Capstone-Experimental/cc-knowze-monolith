# Generated by Django 4.2.7 on 2023-11-29 15:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0002_keyword_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('no', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('img_url', models.TextField()),
            ],
        ),
    ]
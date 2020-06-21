# Generated by Django 2.0.5 on 2020-06-05 11:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='did',
            field=models.CharField(default=uuid.uuid4, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]

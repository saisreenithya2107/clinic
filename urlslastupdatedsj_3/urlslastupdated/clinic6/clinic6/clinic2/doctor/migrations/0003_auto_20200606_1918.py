# Generated by Django 2.0.5 on 2020-06-06 13:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_auto_20200605_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='did',
            field=models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
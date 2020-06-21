# Generated by Django 2.0.5 on 2020-06-05 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Madmin',
            fields=[
                ('maid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('firstname', models.CharField(max_length=150)),
                ('lastname', models.CharField(max_length=150)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='otp_verify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('otp', models.IntegerField(default=0)),
            ],
        ),
    ]
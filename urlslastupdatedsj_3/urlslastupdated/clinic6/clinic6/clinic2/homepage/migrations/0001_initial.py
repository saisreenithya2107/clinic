# Generated by Django 2.0.5 on 2020-06-05 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('aid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('link', models.CharField(blank=True, max_length=150, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('atype', models.IntegerField(blank=True, null=True)),
                ('symptoms', models.CharField(max_length=150)),
                ('reports', models.FileField(blank=True, null=True, upload_to='media')),
                ('status', models.BooleanField(default=False)),
                ('prescription', models.FileField(blank=True, null=True, upload_to='media')),
                ('doctor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='doctor.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='labAppointment',
            fields=[
                ('lappid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('prescription', models.FileField(blank=True, null=True, upload_to='media')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('report', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('ltid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('lab_name', models.CharField(max_length=150)),
                ('email_id', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_num', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('mid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('strength', models.CharField(blank=True, max_length=20, null=True)),
                ('about', models.CharField(default='0000000', max_length=1000)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('prandial', models.CharField(blank=True, max_length=150, null=True)),
                ('times', models.CharField(blank=True, max_length=10, null=True)),
                ('period', models.CharField(blank=True, max_length=10, null=True)),
                ('price', models.FloatField()),
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
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('pid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('firstname', models.CharField(max_length=150)),
                ('lastname', models.CharField(max_length=150)),
                ('pat_photo', models.FileField(null=True, upload_to='')),
                ('email_id', models.EmailField(blank=True, max_length=150, null=True)),
                ('phone_num', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('purid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(null=True)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('cost', models.IntegerField()),
                ('prescription', models.FileField(blank=True, null=True, upload_to='media')),
                ('medicine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.Medicine', unique=None)),
                ('user_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='homepage.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Tests_info',
            fields=[
                ('tid', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('test_name', models.CharField(max_length=150)),
                ('about', models.TextField(blank=True, null=True)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='user_reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='media')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='homepage.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='labtest',
            name='tests_available',
            field=models.ManyToManyField(to='homepage.Tests_info'),
        ),
        migrations.AddField(
            model_name='labappointment',
            name='lab_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='homepage.LabTest'),
        ),
        migrations.AddField(
            model_name='labappointment',
            name='test_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='homepage.Tests_info'),
        ),
        migrations.AddField(
            model_name='labappointment',
            name='user_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='homepage.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='homepage.Patient'),
        ),
    ]

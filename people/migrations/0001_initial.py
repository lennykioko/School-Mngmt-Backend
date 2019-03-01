# Generated by Django 2.1.5 on 2019-02-28 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('id_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=255, null=True)),
                ('profession', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('registration_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('joined_at', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=255, null=True)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('class_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.ClassRoom')),
                ('guardians', models.ManyToManyField(blank=True, to='people.Guardian')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('id_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=255, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('joined_at', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('subjects', models.ManyToManyField(blank=True, to='people.Subject')),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='class_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Teacher'),
        ),
    ]

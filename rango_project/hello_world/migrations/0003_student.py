# Generated by Django 2.1.5 on 2019-01-12 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0002_auto_20190111_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('erno', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('city', models.CharField(max_length=128)),
                ('dob', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('phone', models.IntegerField()),
            ],
        ),
    ]
# Generated by Django 2.1.5 on 2019-01-15 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0007_auto_20190115_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
# Generated by Django 2.1.5 on 2019-01-15 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0005_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]

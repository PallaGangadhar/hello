# Generated by Django 2.1.5 on 2019-01-12 06:58

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0004_auto_20190112_0529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('cat', models.ForeignKey(on_delete=builtins.id, to='hello_world.category')),
            ],
        ),
    ]
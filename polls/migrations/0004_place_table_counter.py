# Generated by Django 2.1.14 on 2020-04-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_remove_place_table_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='place_table',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]

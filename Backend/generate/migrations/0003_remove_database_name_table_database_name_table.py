# Generated by Django 4.1.4 on 2022-12-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0002_remove_database_name_table_database_name_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database_name',
            name='table',
        ),
        migrations.AddField(
            model_name='database_name',
            name='table',
            field=models.ManyToManyField(blank=True, null=True, to='generate.table_name'),
        ),
    ]

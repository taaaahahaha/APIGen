# Generated by Django 4.1.4 on 2022-12-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0005_temp_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-13 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_database_credentials_auth_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='database_credentials',
            name='file_slug',
            field=models.CharField(blank=True, default='xyz', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='database_credentials',
            name='file_type',
            field=models.CharField(blank=True, default='xyz', max_length=100, null=True),
        ),
    ]
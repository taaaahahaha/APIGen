from django.db import models
from django.contrib.auth.models import User

class Database_credentials(models.Model):
    # auth_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    auth_user = models.CharField(max_length=100, blank=True, null=True)
    db_type = models.CharField(max_length=100, blank=True, null=True)

    # For db_type = mysql
    host = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    database = models.CharField(max_length=100, blank=True, null=True)

    # For db_type = mongodb
    mongourl = models.CharField(max_length=1000, blank=True, null=True)
    # database (Already mentioned)

    file_slug = models.CharField(max_length=100, blank=True, null=True, default='xyz')
    file_type = models.CharField(max_length=100, blank=True, null=True, default='xyz')

    def __str__(self):
        return f'{self.auth_user} - {self.db_type}'


# class Basic_auth(models.Model):
#     auth_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
#     is_logged_in = models.BooleanField(default=False)
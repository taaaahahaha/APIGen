from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

# class Table_Name(models.Model):

#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return f'{self.name}'

# class Database_Name(models.Model):

#     name = models.CharField(max_length=100)
#     table = models.ManyToManyField(Table_Name,blank=True,null=True)

#     def __str__(self):
#         return f'{self.name}'


class Results(models.Model):

    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    auth_user = models.CharField(max_length=100,blank=True,null=True)
    file_slug = models.CharField(max_length=100,blank=True,null=True)
    db_type = models.CharField(max_length=100,blank=True,null=True,default='xyz')
    db_name = models.CharField(max_length=100,blank=True,null=True,default='xyz')
    freq_insert_query = models.CharField(max_length=1000,blank=True,null=True)
    freq_select_query = models.CharField(max_length=1000,blank=True,null=True)
    freq_update_query = models.CharField(max_length=1000,blank=True,null=True)
    freq_delete_query = models.CharField(max_length=1000,blank=True,null=True)
    min_time = models.CharField(max_length=1000,blank=True,null=True)
    max_time = models.CharField(max_length=1000,blank=True,null=True)
    mean_time = models.CharField(max_length=1000,blank=True,null=True)
    freq_tables = models.CharField(max_length=1000,blank=True,null=True)

    analytics = JSONField(blank=True,null=True)

    def __str__(self):
        return f'{self.auth_user} - {self.file_slug}'

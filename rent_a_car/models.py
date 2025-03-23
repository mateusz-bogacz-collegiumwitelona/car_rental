# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    street_number = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.city}, {self.street} {self.street_number}"
    class Meta:
        db_table = 'city'

class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    pesel = models.CharField(unique=True, max_length=11)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    id_city = models.ForeignKey(City, db_column='id_city', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"
    class Meta:
        db_table = 'users'

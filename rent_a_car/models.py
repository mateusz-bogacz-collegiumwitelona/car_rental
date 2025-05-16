# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'admin'

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Auta(models.Model):
    id_auta = models.AutoField(primary_key=True)
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    rocznik = models.IntegerField()
    opis = models.CharField(max_length=1000, blank=True, null=True)
    osiagi = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auta'

    def __str__(self):
        return f"{self.marka} {self.model}"

class AutaZdj(models.Model):
    id_zdj = models.AutoField(primary_key=True)
    id_auta = models.ForeignKey(Auta, models.DO_NOTHING, db_column='id_auta')
    zdj = models.CharField(max_length=255)
    kolejnosc = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auta_zdj'
        ordering = ['kolejnosc']


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CzarnaLista(models.Model):
    id_bl = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Uzytkownicy', models.DO_NOTHING, db_column='id_user')
    powod = models.CharField(max_length=50)
    data_poczatkowa = models.DateField()
    data_koncowa = models.DateField()
    id_admin = models.ForeignKey(Admin, models.DO_NOTHING, db_column='id_admin')

    class Meta:
        managed = False
        db_table = 'czarna_lista'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Miasta(models.Model):
    id_zamieszkania = models.AutoField(primary_key=True)
    miasto = models.CharField(max_length=100)
    ulica = models.CharField(max_length=100)
    nr_ulicy = models.CharField(max_length=5)
    kod_pocztowy = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'miasta'
    
    def __str__(self):
        return f"{self.miasto} {self.ulica} {self.nr_ulicy}"


class Uzytkownicy(models.Model):
    id_user = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    pesel = models.CharField(db_column='PESEL', max_length=11, unique=True)
    email = models.CharField(max_length=50, unique=True)
    haslo = models.CharField(max_length=100)
    id_zamieszkania = models.ForeignKey(Miasta, models.DO_NOTHING, db_column='id_zamieszkania')

    class Meta:
        managed = False
        db_table = 'uzytkownicy'
    
    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Wypozyczenie(models.Model):
    id_wypozyczenia = models.AutoField(primary_key=True)
    data_poczatkowa = models.DateField()
    data_koncowa = models.DateField()
    id_auta = models.ForeignKey(Auta, models.DO_NOTHING, db_column='id_auta')
    id_user = models.ForeignKey(Uzytkownicy, models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'wypozyczenie'

class HistoriaZmian(models.Model):
    id_historii = models.AutoField(primary_key=True)
    tabela_zrodlowa = models.CharField(max_length=50)
    id_rekordu = models.IntegerField()
    operacja = models.CharField(max_length=10)
    data_operacji = models.DateTimeField(blank=True, null=True)
    miasto = models.CharField(max_length=100, blank=True, null=True)
    ulica = models.CharField(max_length=100, blank=True, null=True)
    nr_ulicy = models.CharField(max_length=5, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6, blank=True, null=True)
    id_user = models.IntegerField(blank=True, null=True)
    imie = models.CharField(max_length=100, blank=True, null=True)
    nazwisko = models.CharField(max_length=100, blank=True, null=True)
    pesel = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    id_zamieszkania = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historia_zmian'
    
    def __str__(self):
        return f"Historia {self.operacja} - {self.tabela_zrodlowa} (ID: {self.id_historii})"
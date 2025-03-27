from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('admin/flota/', views.zarzadzaj_flota, name='zarzadzaj_flota'),
    path('admin/adresy/', views.zarzadzaj_adresami, name='zarzadzaj_adresami'),
    path('admin/wypozyczenia/', views.zarzadzaj_wypozyczeniami, name='zarzadzaj_wypozyczeniami'),
    path('admin/administratorzy/', views.zarzadzaj_administratorami, name='zarzadzaj_administratorami'),
    path('admin/uzytkownicy/', views.zarzadzaj_uzytkownikami, name='zarzadzaj_uzytkownikami'),
    path('admin/czarna-lista/', views.zarzadzaj_czarna_lista, name='zarzadzaj_czarna_lista'),
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard', views.user_dashboard, name='user_dashboard'),

    path('admin/flota', views.admin_car_view, name='admin_car_view'),
    path('admin/adresy', views.admin_address_view, name='admin_address_view'),
    path('admin/wypozyczenia', views.admin_rent_view, name='admin_rent_view'),
    path('admin/administratorzy', views.admin_admin_view, name='admin_admin_view'),
    path('admin/uzytkownicy', views.admin_user_view, name='admin_user_view'),
    path('admin/czarna-lista', views.admin_blackList_view, name='admin_blackList_view'),
    path('admin/samochod/<int:car_id>/zdjecia', views.admin_car_photos, name='admin_car_photos'),
    path('admin/zdjecia-samochodow/<int:car_id>/', views.admin_car_photos, name='admin_car_photos'),
    path('admin/samochod/<int:car_id>/', views.admin_car_detail, name='admin_car_detail'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('ban-info/', views.user_ban_info, name='user_ban_info'),
    path('rent-car/<int:car_id>/', views.rent_car, name='rent_car'),
    path('admin/samochod/<int:car_id>/', views.admin_car_detail, name='admin_car_detail'),
    path('admin/historia-zmian', views.admin_histroy_change_list, name='admin_histroy_change_list')
]


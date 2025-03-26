from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    #path('logout/', views.logout_view, name='logout'),
    path('test-password/', views.test_password, name='test_password'),
    path('password-debug/', views.password_debug, name='password_debug'),
    path('direct-verify/', views.direct_verify, name='direct_verify'),
    path('test-logowanie/', views.test_logowanie, name='test_logowanie'),
    path('debug-admin/', views.debug_admin_password, name='debug_admin'),
    path('hash-debug/', views.hash_debug, name='hash_debug'),
    path('set-and-login/', views.set_and_login, name='set_and_login'),
    path('direct-login/', views.direct_login, name='direct_login'),
    path('db-diagnostics/', views.db_diagnostics, name='db_diagnostics'),
]

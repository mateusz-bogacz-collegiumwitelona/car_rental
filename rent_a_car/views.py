from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from .forms import LoginForm
from .models import Admin, Uzytkownicy
import logging


logger = logging.getLogger(__name__)

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            logger.info(f"Próba logowania - email: {email}")

            try:
                admin = Admin.objects.filter(email=email).first()
                if admin:
                    logger.info(f"Znaleziono admina: {admin.imie} {admin.nazwisko}")
                    logger.info(f"Hasło z bazy: {admin.password}")
                    logger.info(f"Podane hasło: {password}")
                    
                    # Bezpośrednie sprawdzenie z django.contrib.auth.hashers
                    from django.contrib.auth.hashers import check_password
                    direct_result = check_password(password, admin.password)
                    logger.info(f"Bezpośrednie sprawdzenie hasła: {direct_result}")
                    
                    # Sprawdź także przez metodę modelu
                    try:
                        model_result = admin.check_password(password)
                        logger.info(f"Sprawdzenie przez model: {model_result}")
                    except Exception as e:
                        logger.error(f"Błąd podczas sprawdzania hasła przez model: {e}")
                        model_result = False
                    
                    if direct_result:
                        request.session['user_type'] = 'admin'
                        request.session['user_id'] = admin.id_admin
                        logger.info("Logowanie udane")
                        return redirect('admin_dashboard')
                    else:
                        logger.warning("Nieprawidłowe hasło")
                        messages.error(request, 'Nieprawidłowy email lub hasło')
                else:
                    # Sprawdź użytkownika
                    user = Uzytkownicy.objects.filter(email=email).first()
                    if user:
                        # Sprawdź hasło użytkownika
                        from django.contrib.auth.hashers import check_password
                        if check_password(password, user.haslo):
                            request.session['user_type'] = 'user'
                            request.session['user_id'] = user.id_user
                            logger.info("Logowanie użytkownika udane")
                            return redirect('user_dashboard')
                        else:
                            logger.warning("Nieprawidłowe hasło użytkownika")
                            messages.error(request, 'Nieprawidłowy email lub hasło')
                    else:
                        logger.warning(f"Nie znaleziono użytkownika z emailem: {email}")
                        messages.error(request, 'Nieprawidłowy email lub hasło')
            except Exception as e:
                logger.error(f"Błąd podczas logowania: {e}")
                messages.error(request, 'Wystąpił błąd podczas logowania')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def admin_dashboard(request):
    # Sprawdź czy użytkownik jest zalogowany jako admin
    if request.session.get('user_type') != 'admin':
        return redirect('login')
    
    print(f"Trying to render template: admin_dashboard.html")
    return render(request, 'admin-dashboard.html')

def user_dashboard(request):
    # Sprawdź czy użytkownik jest zalogowany
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    return render(request, 'user_dashboard.html')

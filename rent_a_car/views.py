from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from .forms import LoginForm
from .models import Admin, Uzytkownicy
import logging


logger = logging.getLogger(__name__)


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
    
    return render(request, 'admin_dashboard.html')

def user_dashboard(request):
    # Sprawdź czy użytkownik jest zalogowany
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    return render(request, 'user_dashboard.html')

                    
def test_password(request):
    # Utwórz nowe hasło
    test_pwd = "test123"
    hashed_pwd = make_password(test_pwd)
    
    # Sprawdź czy weryfikacja działa bezpośrednio
    verification = check_password(test_pwd, hashed_pwd)
    
    # Zaktualizuj hasło admina
    try:
        admin = Admin.objects.get(email='admin@adin.pl')
        admin.password = hashed_pwd
        admin.save()
        
        # Sprawdź czy możemy zweryfikować hasło poprzez model
        model_verification = admin.check_password(test_pwd)
        
        return HttpResponse(
            f"Test hasła:<br>"
            f"Oryginalne hasło: {test_pwd}<br>"
            f"Hash: {hashed_pwd}<br>"
            f"Bezpośrednia weryfikacja: {verification}<br>"
            f"Weryfikacja przez model: {model_verification}<br>"
            f"Teraz hasło admina zostało ustawione na: {test_pwd}"
        )
    except Exception as e:
        return HttpResponse(f"Wystąpił błąd: {e}")
    
def password_debug(request):
    try:
        admin = Admin.objects.get(email='admin@adin.pl')
        
        # Sprawdź obecny hash
        current_hash = admin.password
        is_usable = is_password_usable(current_hash)
        
        # Stwórz nowy hash i porównaj z istniejącym
        new_hash = make_password('test123')
        check_result = check_password('test123', current_hash)
        
        # Aktualizuj hasło i zachowaj
        admin.set_password('test123')
        admin.save()
        
        # Sprawdź ponownie po aktualizacji
        updated_admin = Admin.objects.get(email='admin@adin.pl')
        updated_check = check_password('test123', updated_admin.password)
        
        return HttpResponse(
            f"<h2>Informacje o haśle admina</h2>"
            f"<p>Format hasła możliwy do użycia: {is_usable}</p>"
            f"<p>Obecny hash: {current_hash}</p>"
            f"<p>Nowy hash: {new_hash}</p>"
            f"<p>Wynik weryfikacji przed aktualizacją: {check_result}</p>"
            f"<p>Wynik weryfikacji po aktualizacji: {updated_check}</p>"
        )
    except Exception as e:
        return HttpResponse(f"Błąd: {e}")
    
def direct_verify(request):
    try:
        from django.contrib.auth.hashers import make_password, check_password
        
        # Utwórz nowy hash i zweryfikuj go bezpośrednio
        password = 'test123'
        hash_value = make_password(password)
        verification = check_password(password, hash_value)
        
        # Pobierz admina i zaktualizuj jego hasło
        admin = Admin.objects.get(email='admin@adin.pl')
        admin.set_password('test123')
        admin.save()    
        
        
        return HttpResponse(
            f"<h2>Bezpośrednia weryfikacja hasła</h2>"
            f"<p>Hasło: {password}</p>"
            f"<p>Hash: {hash_value}</p>"
            f"<p>Weryfikacja bezpośrednia: {verification}</p>"
            f"<p>Hasło admina zostało zaktualizowane. Spróbuj zalogować się z hasłem: {password}</p>"
            f"<a href='/login/'>Przejdź do logowania</a>"
        )
    except Exception as e:
        return HttpResponse(f"Błąd: {e}")
    
def test_logowanie(request):
    # Pobierz admina
    admin = Admin.objects.get(email='admin@adin.pl')
    
    # Sprawdź hasło bezpośrednio
    from django.contrib.auth.hashers import check_password, make_password
    
    # Testuj różne hasła
    test_password = 'test123'
    wrong_password = 'wrong123'
    
    # Sprawdź aktualne hasło w bazie
    is_current_hash = check_password(test_password, admin.password)
    
    # Twórz nowy hash i zapisz
    admin.set_password(test_password)
    admin.save()
    
    # Pobierz admina ponownie po zapisie
    admin_updated = Admin.objects.get(email='admin@adin.pl')
    is_updated_hash = check_password(test_password, admin_updated.password)
    
    # Sprawdź metodą modelu
    model_check = admin_updated.check_password(test_password)
    
    return HttpResponse(
        f"<h1>Test logowania admina</h1>"
        f"<p>Email admina: {admin.email}</p>"
        f"<p>Hasło w bazie: {admin.password}</p>"
        f"<p>Hasło testowe: {test_password}</p>"
        f"<p>Sprawdzenie obecnego hasła: {is_current_hash}</p>"
        f"<p>Nowe hasło po zapisie: {admin_updated.password}</p>"
        f"<p>Sprawdzenie nowego hasła: {is_updated_hash}</p>"
        f"<p>Sprawdzenie metodą modelu: {model_check}</p>"
        f"<p><a href='/login/'>Przejdź do logowania</a></p>"
    )

def debug_admin_password(request):
    try:
        # Sprawdź wszystkich adminów
        admins = Admin.objects.all()
        admin_info = []
        
        for admin in admins:
            admin_info.append({
                'id': admin.id_admin,
                'email': admin.email,
                'name': f"{admin.imie} {admin.nazwisko}",
                'password_hash': admin.password
            })
        
        # Testuj aktualizację na konkretnym adminie
        target_admin = Admin.objects.get(email='admin@adin.pl')
        old_hash = target_admin.password
        
        # Aktualizuj hasło
        test_hash = make_password('test123')
        target_admin.password = test_hash
        target_admin.save()
        
        # Sprawdź czy zmiana została zapisana
        updated_admin = Admin.objects.get(id_admin=target_admin.id_admin)
        
        html_response = "<h1>Admin Debug Info</h1>"
        html_response += f"<h2>All Admins ({len(admin_info)})</h2>"
        html_response += "<ul>"
        for info in admin_info:
            html_response += f"<li>ID: {info['id']}, Email: {info['email']}, Name: {info['name']}<br>Hash: {info['password_hash']}</li>"
        html_response += "</ul>"
        
        html_response += "<h2>Password Update Test</h2>"
        html_response += f"<p>Target Admin ID: {target_admin.id_admin}</p>"
        html_response += f"<p>Old Hash: {old_hash}</p>"
        html_response += f"<p>New Hash: {test_hash}</p>"
        html_response += f"<p>Saved Hash: {updated_admin.password}</p>"
        html_response += f"<p>Hash Match: {test_hash == updated_admin.password}</p>"
        
        return HttpResponse(html_response)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
def hash_debug(request):
    from django.contrib.auth.hashers import make_password, check_password
    
    # Stwórz nowy hash dla hasła test123
    test_password = 'test123'
    new_hash = make_password(test_password)
    
    # Pobierz aktualny hash admina
    admin = Admin.objects.get(email='admin@adin.pl')
    admin_hash = admin.password
    
    # Sprawdź bezpośrednio
    direct_check = check_password(test_password, admin_hash)
    
    # Sprawdź szczegóły haszy
    admin_hash_parts = admin_hash.split('$') if '$' in admin_hash else []
    new_hash_parts = new_hash.split('$') if '$' in new_hash else []
    
    # Aktualizuj hasło bezpośrednio w bazie danych
    from django.db import connection
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE admin SET password = %s WHERE email = %s",
            [new_hash, 'admin@adin.pl']
        )
        connection.commit()
        db_update_status = "Aktualizacja bazy danych zakończona pomyślnie"
    except Exception as e:
        db_update_status = f"Błąd aktualizacji bazy danych: {str(e)}"
    
    # Pobierz admina ponownie
    admin_updated = Admin.objects.get(email='admin@adin.pl')
    updated_hash = admin_updated.password
    
    response = f"""
    <h1>Debugowanie Hasła</h1>
    <p>Oryginalne hasło: {test_password}</p>
    <p>Wygenerowany hash: {new_hash}</p>
    <p>Hash w bazie danych: {admin_hash}</p>
    <p>Bezpośrednia weryfikacja: {direct_check}</p>
    
    <h2>Szczegóły haszy</h2>
    <p>Hash admina - części: {len(admin_hash_parts)}</p>
    <ol>
    """
    
    for i, part in enumerate(admin_hash_parts):
        response += f"<li>Część {i}: {part}</li>"
    
    response += """
    </ol>
    <p>Nowy hash - części: {len(new_hash_parts)}</p>
    <ol>
    """
    
    for i, part in enumerate(new_hash_parts):
        response += f"<li>Część {i}: {part}</li>"
    
    response += f"""
    </ol>
    
    <h2>Aktualizacja SQL</h2>
    <p>{db_update_status}</p>
    <p>Hash po aktualizacji SQL: {updated_hash}</p>
    <p>Porównanie raw hashów: {'IDENTYCZNE' if admin_hash == updated_hash else 'RÓŻNE'}</p>
    <p>Porównanie update vs new: {'IDENTYCZNE' if updated_hash == new_hash else 'RÓŻNE'}</p>
    
    <h2>Klasa modelu Admin</h2>
    <pre>
    {Admin.__module__}.{Admin.__name__}
    check_password method: {getattr(Admin, 'check_password', 'Nie znaleziono')}
    </pre>
    
    <p><a href="/login/">Przejdź do strony logowania</a></p>
    """
    
    return HttpResponse(response)

def direct_login(request):
    """Strona logowania z autouzupełnionym hasłem (tylko do testów)"""
    temp_password = request.session.get('temp_password', '')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Standardowa logika logowania
            # Ale używaj tylko bezpośredniego sprawdzenia
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            admin = Admin.objects.filter(email=email).first()
            if admin:
                from django.contrib.auth.hashers import check_password
                if check_password(password, admin.password):
                    request.session['user_type'] = 'admin'
                    request.session['user_id'] = admin.id_admin
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Nieprawidłowe hasło')
            else:
                messages.error(request, 'Nie znaleziono admina')
    else:
        form = LoginForm(initial={'email': 'admin@adin.pl'})
    
    return render(request, 'direct_login.html', {'form': form, 'temp_password': temp_password})

def set_and_login(request):
    try:
        # Zaktualizuj hasło admina
        admin = Admin.objects.get(email='admin@adin.pl')
        
        # Ustaw tymczasowe proste hasło dla testów
        password = 'test123'
        
        # Użyj bezpośrednio funkcji make_password
        from django.contrib.auth.hashers import make_password
        admin.password = make_password(password)
        admin.save()
        
        # Zapisz hasło w sesji (tylko dla tego testu)
        request.session['temp_password'] = password
        
        # Przekieruj do specjalnej strony logowania
        return redirect('direct_login')
    except Exception as e:
        return HttpResponse(f"Błąd: {str(e)}")
    

def db_diagnostics(request):
    """Funkcja do diagnozowania problemów z bazą danych"""
    from django.db import connection, transaction
    from django.contrib.auth.hashers import make_password, check_password
    
    results = []
    
    # 1. Sprawdź połączenie do bazy
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            results.append(("Połączenie do bazy", "Działa"))
    except Exception as e:
        results.append(("Połączenie do bazy", f"Błąd: {str(e)}"))
    
    # 2. Sprawdź strukturę tabeli admin
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'admin'
            """)
            columns = cursor.fetchall()
            results.append(("Struktura tabeli admin", str(columns)))
    except Exception as e:
        results.append(("Struktura tabeli admin", f"Błąd: {str(e)}"))
    
    # 3. Sprawdź aktualne hasło admina
    try:
        admin = Admin.objects.get(email='admin@adin.pl')
        results.append(("Aktualne hasło admina", admin.password))
        results.append(("Długość hasła admina", str(len(admin.password))))
    except Exception as e:
        results.append(("Aktualne hasło admina", f"Błąd: {str(e)}"))
    
    # 4. Spróbuj zaktualizować hasło bezpośrednio przez SQL
    try:
        test_hash = make_password('test123')
        results.append(("Nowy hash", test_hash))
        results.append(("Długość nowego hasza", str(len(test_hash))))
        
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE admin SET password = %s WHERE email = %s",
                    [test_hash, 'admin@adin.pl']
                )
                rows_affected = cursor.rowcount
                results.append(("Aktualizacja SQL", f"Wykonano, zaktualizowano {rows_affected} wierszy"))
        
        # Sprawdź czy zmiany zostały zapisane
        admin_reloaded = Admin.objects.get(email='admin@adin.pl')
        updated_hash = admin_reloaded.password
        results.append(("Hash po aktualizacji SQL", updated_hash))
        results.append(("Długość hasła po aktualizacji", str(len(updated_hash))))
        results.append(("Czy hash został zmieniony", "TAK" if updated_hash == test_hash else "NIE"))
        
        # Sprawdź czy weryfikacja działa
        verify_result = check_password('test123', updated_hash)
        results.append(("Weryfikacja po SQL", str(verify_result)))
        
        # Test przez metodę modelu
        model_verify = admin_reloaded.check_password('test123')
        results.append(("Weryfikacja przez model", str(model_verify)))
    except Exception as e:
        results.append(("Aktualizacja SQL", f"Błąd: {str(e)}"))
    
    # 5. Sprawdź ustawienia zarządzania modelami
    results.append(("Admin.Meta.managed", str(Admin._meta.managed)))
    
    # 6. Sprawdź bezpośrednio w bazie danych
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM admin WHERE email = %s", ['admin@adin.pl'])
            db_password = cursor.fetchone()[0]
            results.append(("Hasło bezpośrednio z bazy", db_password))
            results.append(("Długość hasła z bazy", str(len(db_password))))
    except Exception as e:
        results.append(("Zapytanie bezpośrednie", f"Błąd: {str(e)}"))
    
    # Renderuj wyniki
    html_output = "<h1>Diagnostyka Bazy Danych</h1><table border='1'>"
    for name, value in results:
        html_output += f"<tr><td><strong>{name}</strong></td><td>{value}</td></tr>"
    html_output += "</table>"
    
    return HttpResponse(html_output)
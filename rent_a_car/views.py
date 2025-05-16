import logging
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from datetime import datetime
import os

from .forms import (
    LoginForm, CarForm, CityForm, UserForm,
    AdminForm, RentForm, BlackListForm, RegistrationForm, 
)
from .models import Auta, AutaZdj

from .services.user_service import UserService
from .services.car_service import CarService
from .services.rental_service import RentalService
from .services.admin_service import AdminService
from .services.blacklist_service import BlacklistService
from .services.change_history_service import ChangeHistoryService

logger = logging.getLogger(__name__)

# Funkcje pomocnicze
def is_admin_logged_in(request):
    return request.session.get('user_type') == 'admin' and request.session.get('user_id')

def is_user_logged_in(request):
    return request.session.get('user_type') == 'user' and request.session.get('user_id')

# Widok strony głównej
def index_view(request):
    return render(request, 'index.html')

# Administracja - Dashboard
def admin_dashboard(request):
    if not is_admin_logged_in(request):
        return redirect('login')
    return render(request, 'admin/admin-dashboard.html')

# Użytkownik - Dashboard
def user_dashboard(request):
    if not is_user_logged_in(request):
        return redirect('login')
    
    user_id = request.session.get('user_id')

    if UserService.is_blacklisted(user_id):
        return redirect('user_ban_info')
    
    cars = CarService.get_all_cars_with_status()
    
    return render(request, 'user/user_dashboard.html', {'cars': cars})

# Logowanie
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            admin = AdminService.authenticate_admin(email, password)
            if admin:
                request.session['user_type'] = 'admin'
                request.session['user_id'] = admin.id_admin
                return redirect('admin_dashboard')
            
            user = UserService.authenticate_user(email, password)
            if user:
                request.session['user_type'] = 'user'
                request.session['user_id'] = user.id_user
                return redirect('user_dashboard')
            
            messages.error(request, 'Nieprawidłowy email lub hasło')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Wylogowanie
def logout_view(request):
    if 'user_type' in request.session:
        del request.session['user_type']
    if 'user_id' in request.session:
        del request.session['user_id']
    
    messages.success(request, 'Zostałeś wylogowany')
    return redirect('login')

# Rejestracja
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = {
                'imie': form.cleaned_data['imie'],
                'nazwisko': form.cleaned_data['nazwisko'],
                'pesel': form.cleaned_data['pesel'],
                'email': form.cleaned_data['email'],
                'haslo': form.cleaned_data['password']
            }
            
            address_data = {
                'miasto': form.cleaned_data['city'],
                'ulica': form.cleaned_data['street'],
                'nr_ulicy': form.cleaned_data['street_numb'],
                'kod_pocztowy': form.cleaned_data['zip_code']
            }

            UserService.create_user(user_data, address_data)
            
            messages.success(request, 'Konto zostało utworzone. Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

# Administracja - Zarządzanie samochodami
def admin_car_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    cars = CarService.get_all_cars()
    form = CarForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = CarForm(request.POST)
            if form.is_valid():  # Upewnij się, że to jest wykonane przed dostępem do cleaned_data
                car_data = {
                    'marka': form.cleaned_data['marka'],
                    'model': form.cleaned_data['model'],
                    'rocznik': form.cleaned_data['rocznik'],
                    'opis': form.cleaned_data['opis'],
                    'osiagi': form.cleaned_data['osiagi']
                }
                CarService.create_car(car_data)
                messages.success(request, 'Auto zostało dodane.')
                return redirect('admin_car_view')
        elif 'usun' in request.POST:
            car_id = request.POST.get('id_auta')
            CarService.delete_car(car_id)
            messages.success(request, 'Auto zostało usunięte.')
            return redirect('admin_car_view')
        elif 'edytuj' in request.POST:
            car_id = request.POST.get('id_auta')
            form = CarForm(request.POST)
            if form.is_valid():  # Tu również potrzebna jest ta linia
                car_data = {
                    'marka': form.cleaned_data['marka'],
                    'model': form.cleaned_data['model'],
                    'rocznik': form.cleaned_data['rocznik'],
                    'opis': form.cleaned_data['opis'],
                    'osiagi': form.cleaned_data['osiagi']
                }
                CarService.update_car(car_id, car_data)
                messages.success(request, 'Auto zostało zaktualizowane.')
                return redirect('admin_car_view')
    
    return render(request, 'admin/admin_car_view.html', {'auta': cars, 'form': form})

# Administracja - Zarządzanie adresami
def admin_address_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    addresses = UserService.get_all_addresses()
    form = CityForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = CityForm(request.POST)
            if form.is_valid():
                address_data = {
                    'miasto': form.cleaned_data['miasto'],
                    'ulica': form.cleaned_data['ulica'],
                    'nr_ulicy': form.cleaned_data['nr_ulicy'],
                    'kod_pocztowy': form.cleaned_data['kod_pocztowy']
                }
                UserService.create_address(address_data)
                messages.success(request, 'Adres został dodany.')
                return redirect('admin_address_view')
        elif 'usun' in request.POST:
            address_id = request.POST.get('id_zamieszkania')
            UserService.delete_address(address_id)
            messages.success(request, 'Adres został usunięty.')
            return redirect('admin_address_view')
        elif 'edytuj' in request.POST:
            address_id = request.POST.get('id_zamieszkania')
            form = CityForm(request.POST)
            if form.is_valid():
                address_data = {
                    'miasto': form.cleaned_data['miasto'],
                    'ulica': form.cleaned_data['ulica'],
                    'nr_ulicy': form.cleaned_data['nr_ulicy'],
                    'kod_pocztowy': form.cleaned_data['kod_pocztowy']
                }
                UserService.update_address(address_id, address_data)
                messages.success(request, 'Adres został zaktualizowany.')
                return redirect('admin_address_view')
    
    return render(request, 'admin/admin_address_view.html', {'miasta': addresses, 'form': form})



# Administracja - Zarządzanie wypożyczeniami
def admin_rent_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    rentals = RentalService.get_all_rentals()
    form = RentForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = RentForm(request.POST)
            if form.is_valid():
                rental_data = {
                    'data_poczatkowa': form.cleaned_data['data_poczatkowa'],
                    'data_koncowa': form.cleaned_data['data_koncowa'],
                    'id_auta_id': form.cleaned_data['id_auta'].id_auta,
                    'id_user_id': form.cleaned_data['id_user'].id_user
                }
                rental, error = RentalService.create_rental(rental_data)
                if rental:
                    messages.success(request, 'Wypożyczenie zostało dodane.')
                else:
                    messages.error(request, error or 'Nie udało się dodać wypożyczenia.')
                return redirect('admin_rent_view')
        elif 'usun' in request.POST:
            rental_id = request.POST.get('id_wypozyczenia')
            RentalService.delete_rental(rental_id)
            messages.success(request, 'Wypożyczenie zostało usunięte.')
            return redirect('admin_rent_view')
        elif 'edytuj' in request.POST:
            rental_id = request.POST.get('id_wypozyczenia')
            form = RentForm(request.POST)
            if form.is_valid():
                rental_data = {
                    'data_poczatkowa': form.cleaned_data['data_poczatkowa'],
                    'data_koncowa': form.cleaned_data['data_koncowa'],
                    'id_auta_id': form.cleaned_data['id_auta'].id_auta,
                    'id_user_id': form.cleaned_data['id_user'].id_user
                }
                RentalService.update_rental(rental_id, rental_data)
                messages.success(request, 'Wypożyczenie zostało zaktualizowane.')
                return redirect('admin_rent_view')
    
    return render(request, 'admin/admin_rent_view.html', {'wypozyczenia': rentals, 'form': form})

# Administracja - Zarządzanie administratorami
def admin_admin_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    admins = AdminService.get_all_admins()
    form = AdminForm()
    
    if request.method == 'POST':
        print("POST request received in admin_admin_view")
        print(f"POST data: {request.POST}")
        
        if 'dodaj' in request.POST:
            form = AdminForm(request.POST)
            print(f"Form is valid: {form.is_valid()}")
            
            if form.is_valid():
                print("Form is valid, attempting to create admin")
                admin_data = {
                    'imie': form.cleaned_data['imie'],
                    'nazwisko': form.cleaned_data['nazwisko'],
                    'email': form.cleaned_data['email']
                }
                password = form.cleaned_data.get('password')
                
                try:
                    admin = AdminService.create_admin(admin_data, password)
                    print(f"Admin created: {admin}")
                    messages.success(request, 'Administrator został dodany.')
                except Exception as e:
                    print(f"Error creating admin: {str(e)}")
                    messages.error(request, f'Błąd podczas dodawania administratora: {str(e)}')
                
                return redirect('admin_admin_view')
            else:
                print(f"Form errors: {form.errors}")
        
        elif 'usun' in request.POST:
            admin_id = request.POST.get('id_admin')
            print(f"Attempting to delete admin with ID: {admin_id}")
            
            # Nie pozwól usunąć zalogowanego administratora
            if int(admin_id) == request.session.get('user_id'):
                messages.error(request, 'Nie możesz usunąć swojego konta!')
                return redirect('admin_admin_view')
            
            try:
                AdminService.delete_admin(admin_id)
                print(f"Admin deleted with ID: {admin_id}")
                messages.success(request, 'Administrator został usunięty.')
            except Exception as e:
                print(f"Error deleting admin: {str(e)}")
                messages.error(request, f'Błąd podczas usuwania administratora: {str(e)}')
            
            return redirect('admin_admin_view')
        
        elif 'edytuj' in request.POST:
            admin_id = request.POST.get('id_admin')
            print(f"Attempting to edit admin with ID: {admin_id}")
            
            form = AdminForm(request.POST)
            print(f"Edit form is valid: {form.is_valid()}")
            
            if form.is_valid():
                admin_data = {
                    'imie': form.cleaned_data['imie'],
                    'nazwisko': form.cleaned_data['nazwisko'],
                    'email': form.cleaned_data['email']
                }
                password = form.cleaned_data.get('password')
                
                try:
                    AdminService.update_admin(admin_id, admin_data, password)
                    print(f"Admin updated with ID: {admin_id}")
                    messages.success(request, 'Administrator został zaktualizowany.')
                except Exception as e:
                    print(f"Error updating admin: {str(e)}")
                    messages.error(request, f'Błąd podczas aktualizacji administratora: {str(e)}')
                
                return redirect('admin_admin_view')
            else:
                print(f"Edit form errors: {form.errors}")
    
    return render(request, 'admin/admin_admin_view.html', {'administratorzy': admins, 'form': form})

# Administracja - Zarządzanie użytkownikami
def admin_user_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    users = UserService.get_all_users()
    form = UserForm()
    
    if request.method == 'POST':
        print("POST request received in admin_user_view")
        print(f"POST data: {request.POST}")
        
        if 'dodaj' in request.POST:
            form = UserForm(request.POST)
            print(f"Form is valid: {form.is_valid()}")
            
            if form.is_valid():
                print("Form is valid, attempting to create user")
                
                # Przygotuj dane użytkownika
                user_data = {
                    'imie': form.cleaned_data['imie'],
                    'nazwisko': form.cleaned_data['nazwisko'],
                    'pesel': form.cleaned_data['pesel'],
                    'email': form.cleaned_data['email'],
                }
                
                # Pobierz hasło i adres zamieszkania
                haslo = form.cleaned_data.get('haslo')
                id_zamieszkania = form.cleaned_data.get('id_zamieszkania')
                
                try:
                    # Hashuj hasło i dodaj do danych użytkownika
                    from django.contrib.auth.hashers import make_password
                    user_data['haslo'] = make_password(haslo)
                    user_data['id_zamieszkania'] = id_zamieszkania
                    
                    # Utwórz użytkownika za pomocą repozytorium
                    from .repositories.user_repository import UserRepository
                    user = UserRepository.create_user(user_data)
                    
                    print(f"User created: {user}")
                    messages.success(request, 'Użytkownik został dodany.')
                except Exception as e:
                    print(f"Error creating user: {str(e)}")
                    messages.error(request, f'Błąd podczas dodawania użytkownika: {str(e)}')
                
                return redirect('admin_user_view')
            else:
                print(f"Form errors: {form.errors}")
        
        elif 'usun' in request.POST:
            user_id = request.POST.get('id_user')
            print(f"Attempting to delete user with ID: {user_id}")
            
            try:
                from .repositories.user_repository import UserRepository
                UserRepository.delete_user(user_id)
                print(f"User deleted with ID: {user_id}")
                messages.success(request, 'Użytkownik został usunięty.')
            except Exception as e:
                print(f"Error deleting user: {str(e)}")
                messages.error(request, f'Błąd podczas usuwania użytkownika: {str(e)}')
            
            return redirect('admin_user_view')
        
        elif 'edytuj' in request.POST:
            user_id = request.POST.get('id_user')
            print(f"Attempting to edit user with ID: {user_id}")
            
            form = UserForm(request.POST)
            print(f"Edit form is valid: {form.is_valid()}")
            
            if form.is_valid():
                user_data = {
                    'imie': form.cleaned_data['imie'],
                    'nazwisko': form.cleaned_data['nazwisko'],
                    'pesel': form.cleaned_data['pesel'],
                    'email': form.cleaned_data['email'],
                    'id_zamieszkania': form.cleaned_data['id_zamieszkania']
                }
                
                haslo = form.cleaned_data.get('haslo')
                
                try:
                    # Aktualizuj użytkownika
                    UserService.update_user(user_id, user_data, haslo)
                    print(f"User updated with ID: {user_id}")
                    messages.success(request, 'Użytkownik został zaktualizowany.')
                except Exception as e:
                    print(f"Error updating user: {str(e)}")
                    messages.error(request, f'Błąd podczas aktualizacji użytkownika: {str(e)}')
                
                return redirect('admin_user_view')
            else:
                print(f"Edit form errors: {form.errors}")
    
    return render(request, 'admin/admin_user_view.html', {'uzytkownicy': users, 'form': form})


# Administracja - Zarządzanie czarną listą
def admin_blackList_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    blacklist = BlacklistService.get_all_blacklist()
    form = BlackListForm()
    
    # Automatycznie ustaw aktualnego administratora jako dodającego
    if request.method == 'GET':
        try:
            admin_id = request.session.get('user_id')
            admin = AdminService.get_admin_by_id(admin_id)
            if admin:
                form = BlackListForm(initial={'id_admin': admin})
        except Exception as e:
            messages.error(request, f'Błąd podczas inicjalizacji formularza: {str(e)}')
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = BlackListForm(request.POST)
            if form.is_valid():
                blacklist_data = {
                    'id_user_id': form.cleaned_data['id_user'].id_user,
                    'powod': form.cleaned_data['powod'],
                    'data_poczatkowa': form.cleaned_data['data_poczatkowa'],
                    'data_koncowa': form.cleaned_data['data_koncowa'],
                    'id_admin_id': form.cleaned_data['id_admin'].id_admin
                }
                BlacklistService.add_to_blacklist(blacklist_data)
                messages.success(request, 'Użytkownik został dodany do czarnej listy.')
                return redirect('admin_blackList_view')
        elif 'usun' in request.POST:
            blacklist_id = request.POST.get('id_bl')
            BlacklistService.delete_blacklist_entry(blacklist_id)
            messages.success(request, 'Wpis został usunięty z czarnej listy.')
            return redirect('admin_blackList_view')
        elif 'edytuj' in request.POST:
            blacklist_id = request.POST.get('id_bl')
            form = BlackListForm(request.POST)
            if form.is_valid():
                blacklist_data = {
                    'id_user_id': form.cleaned_data['id_user'].id_user,
                    'powod': form.cleaned_data['powod'],
                    'data_poczatkowa': form.cleaned_data['data_poczatkowa'],
                    'data_koncowa': form.cleaned_data['data_koncowa'],
                    'id_admin_id': form.cleaned_data['id_admin'].id_admin
                }
                BlacklistService.update_blacklist_entry(blacklist_id, blacklist_data)
                messages.success(request, 'Wpis czarnej listy został zaktualizowany.')
                return redirect('admin_blackList_view')
    
    return render(request, 'admin/admin_blackList_view.html', {'czarna_lista': blacklist, 'form': form})

def car_detail(request, car_id):
    if not is_user_logged_in(request):
        return redirect('login')
    
    user_id = request.session.get('user_id')

    if UserService.is_blacklisted(user_id):
        return redirect('user_ban_info')

    car_details = CarService.get_car_details(car_id)
    if not car_details:
        messages.error(request, 'Nie znaleziono auta.')
        return redirect('user_dashboard')
    
    context = {
        'car': car_details['car'],
        'car_photos': car_details['photos'],
        'available': car_details['available'],
        'rental_history': car_details['rental_history'],
        'today': datetime.now().date()
    }
    
    return render(request, 'user/car_detail.html', context)

# Informacja o banie użytkownika
def user_ban_info(request):
    if not is_user_logged_in(request):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    user = UserService.get_user_by_id(user_id)
    
    # Pobierz aktywny ban
    active_ban = UserService.get_active_ban(user_id)
    
    if not active_ban:
        return redirect('user_dashboard')
    
    context = {
        'user': user,
        'ban': active_ban
    }
    
    return render(request, 'user/user_ban_info.html', context)

# Wypożyczenie auta
def rent_car(request, car_id):
    if not is_user_logged_in(request):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    
    if UserService.is_blacklisted(user_id):
        return redirect('user_ban_info')

    car = CarService.get_car_by_id(car_id)
    if not car:
        messages.error(request, 'Nie znaleziono auta.')
        return redirect('user_dashboard')
    
    if not CarService.is_car_available(car_id):
        messages.error(request, 'To auto jest obecnie niedostępne.')
        return redirect('car_detail', car_id=car_id)
    
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            rental_data = {
                'data_poczatkowa': form.cleaned_data['data_poczatkowa'],
                'data_koncowa': form.cleaned_data['data_koncowa'],
                'id_auta_id': car_id,
                'id_user_id': user_id
            }
            
            rental, error = RentalService.create_rental(rental_data)
            if rental:
                messages.success(request, 'Auto zostało wypożyczone.')
                return redirect('user_dashboard')
            else:
                messages.error(request, error or 'Nie udało się wypożyczyć auta.')
    else:
        initial_data = {
            'data_poczatkowa': datetime.now().date()
        }
        form = RentForm(initial=initial_data)
    
    context = {
        'car': car,
        'form': form
    }
    
    return render(request, 'user/rent_car.html', context)

# Administracja - Zarządzanie zdjęciami samochodów
def admin_car_photos(request, car_id):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    car = CarService.get_car_by_id(car_id)
    if not car:
        messages.error(request, 'Nie znaleziono auta.')
        return redirect('admin_car_view')
    
    photos = CarService.get_car_photos(car_id)
    available_images = CarService.get_available_images()
    
    if request.method == 'POST':
        # Obsługa dodawania istniejącego zdjęcia
        if 'add_photo' in request.POST:
            selected_image = request.POST.get('selected_image')
            if selected_image:
                if len(photos) >= 5:
                    messages.error(request, 'Maksymalna liczba zdjęć dla jednego auta to 5.')
                else:
                    photo_data = {
                        'id_auta_id': car_id,
                        'zdj': f'cars/{selected_image}',
                        'kolejnosc': len(photos) + 1,
                        'created_at': datetime.now()
                    }
                    CarService.add_car_photo(car_id, photo_data)
                    messages.success(request, 'Zdjęcie zostało dodane.')
                    return redirect('admin_car_photos', car_id=car_id)
            else:
                messages.error(request, 'Nie wybrano zdjęcia.')
        
        # Obsługa dodawania nowego zdjęcia z komputera
        elif 'upload_photo' in request.POST and request.FILES.get('upload_image'):
            if len(photos) >= 5:
                messages.error(request, 'Maksymalna liczba zdjęć dla jednego auta to 5.')
            else:
                try:
                    # Obsługa przesyłanego pliku
                    uploaded_image = request.FILES['upload_image']
                    
                    # Sprawdzenie czy plik jest obrazem na podstawie rozszerzenia
                    import os
                    file_ext = os.path.splitext(uploaded_image.name)[1].lower()
                    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
                    
                    if file_ext not in allowed_extensions:
                        messages.error(request, 'Wybrany plik nie jest obrazem. Dozwolone formaty to: JPG, PNG, GIF, BMP.')
                        return redirect('admin_car_photos', car_id=car_id)
                    
                    # Generowanie unikalnej nazwy pliku
                    from django.utils.text import slugify
                    filename = f"{slugify(car.marka)}_{slugify(car.model)}_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_ext}"
                    
                    # Ścieżka zapisu
                    from django.conf import settings
                    
                    # Upewnij się, że katalog istnieje
                    cars_dir = os.path.join(settings.MEDIA_ROOT, 'cars')
                    os.makedirs(cars_dir, exist_ok=True)
                    
                    # Pełna ścieżka zapisu
                    file_path = os.path.join(cars_dir, filename)
                    
                    # Zapisz plik
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_image.chunks():
                            destination.write(chunk)
                    
                    # Dodaj zdjęcie do bazy danych
                    photo_data = {
                        'id_auta_id': car_id,
                        'zdj': f'cars/{filename}',
                        'kolejnosc': len(photos) + 1,
                        'created_at': datetime.now()
                    }
                    CarService.add_car_photo(car_id, photo_data)
                    messages.success(request, 'Zdjęcie zostało pomyślnie wgrane i dodane.')
                    return redirect('admin_car_photos', car_id=car_id)
                
                except Exception as e:
                    messages.error(request, f'Wystąpił błąd podczas wgrywania zdjęcia: {str(e)}')
        
        # Obsługa usuwania zdjęcia
        elif 'delete_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            if photo_id:
                try:
                    # Znajdź zdjęcie przed usunięciem, aby poznać jego kolejność
                    from .models import AutaZdj
                    photo = AutaZdj.objects.get(id_zdj=photo_id)
                    deleted_order = photo.kolejnosc
                    
                    # Usuń zdjęcie
                    CarService.delete_car_photo(photo_id)
                    
                    # Aktualizacja kolejności pozostałych zdjęć
                    remaining_photos = AutaZdj.objects.filter(id_auta=car_id).order_by('kolejnosc')
                    for i, photo in enumerate(remaining_photos, 1):
                        if photo.kolejnosc != i:
                            photo.kolejnosc = i
                            photo.save()
                    
                    messages.success(request, 'Zdjęcie zostało usunięte.')
                except Exception as e:
                    messages.error(request, f'Wystąpił błąd podczas usuwania zdjęcia: {str(e)}')
            return redirect('admin_car_photos', car_id=car_id)
        
        # Obsługa zmiany kolejności zdjęcia
        elif 'change_order' in request.POST:
            photo_id = request.POST.get('photo_id')
            new_order = request.POST.get('new_order')
            
            if photo_id and new_order:
                try:
                    from .models import AutaZdj
                    from django.db import models
                    
                    photo_to_update = AutaZdj.objects.get(id_zdj=photo_id)
                    old_order = photo_to_update.kolejnosc
                    new_order = int(new_order)
                    
                    # Jeśli nowa kolejność jest taka sama, nic nie rób
                    if old_order == new_order:
                        return redirect('admin_car_photos', car_id=car_id)
                    
                    # Zaktualizuj kolejność innych zdjęć
                    if old_order < new_order:
                        # Przesuwanie w dół
                        AutaZdj.objects.filter(
                            id_auta=car_id, 
                            kolejnosc__gt=old_order, 
                            kolejnosc__lte=new_order
                        ).update(kolejnosc=models.F('kolejnosc') - 1)
                    else:
                        # Przesuwanie w górę
                        AutaZdj.objects.filter(
                            id_auta=car_id, 
                            kolejnosc__lt=old_order, 
                            kolejnosc__gte=new_order
                        ).update(kolejnosc=models.F('kolejnosc') + 1)
                    
                    # Ustaw nową kolejność dla aktualizowanego zdjęcia
                    photo_to_update.kolejnosc = new_order
                    photo_to_update.save()
                    
                    messages.success(request, 'Kolejność zdjęć została zaktualizowana.')
                except Exception as e:
                    messages.error(request, f'Wystąpił błąd podczas zmiany kolejności: {str(e)}')
            
            return redirect('admin_car_photos', car_id=car_id)
    
    context = {
        'car': car,
        'photos': photos,
        'available_images': available_images,
    }
    
    return render(request, 'admin/admin_car_photos.html', context)

# Administracja - Szczegóły auta
def admin_car_detail(request, car_id):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    car = CarService.get_car_by_id(car_id)
    if not car:
        messages.error(request, 'Nie znaleziono auta.')
        return redirect('admin_car_view')
    
    photos = CarService.get_car_photos(car_id)
    
    if request.method == 'POST':
        if 'add_photo' in request.POST and 'photo' in request.FILES:
            pass
        elif 'delete_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            CarService.delete_car_photo(photo_id)
            messages.success(request, 'Zdjęcie zostało usunięte.')
            return redirect('admin_car_detail', car_id=car_id)
        elif 'edit_car' in request.POST:
            form = CarForm(request.POST)
            if form.is_valid():
                car_data = {
                    'marka': form.cleaned_data['marka'],
                    'model': form.cleaned_data['model'],
                    'rocznik': form.cleaned_data['rocznik'],
                    'opis': form.cleaned_data['opis'],
                    'osiagi': form.cleaned_data['osiagi']
                }
                CarService.update_car(car_id, car_data)
                messages.success(request, 'Auto zostało zaktualizowane.')
                return redirect('admin_car_detail', car_id=car_id)
    else:
        form = CarForm(instance=car)
    
    context = {
        'car': car,
        'photos': photos,
        'form': form,
        'active_tab': request.GET.get('tab', 'info')
    }
    
    return render(request, 'admin/admin_car_detail.html', context)

def admin_histroy_change_list(request):
    service = ChangeHistoryService()

    if 'export_csv' in request.GET:
        params = {}
        
        for field in ['tabela_zrodlowa', 'operacja', 'miasto', 'id_user']:
            if request.GET.get(field):
                params[field] = request.GET.get(field)

        if params:
            histroy_change = service.filter_history_change(params)
        else:
            histroy_change = service.get_all_history_change()
            
        return service.export_to_csv(histroy_change)
    
    params = {}
    
    for field in ['tabela_zrodlowa', 'operacja', 'miasto', 'id_user']:
        if request.GET.get(field):
            params[field] = request.GET.get(field)
    
    if params:
        histroy_change = service.filter_history_change(params)
    else:
        histroy_change = service.get_all_history_change()

    context = {
        'historia_zmian_list': histroy_change,
        'title': 'Historia zmian'
    }
    
    return render(request, 'admin/admin_history_change_list.html', context)


# Obsługa błędów
def handler404(request, exception):
    return render(request, 'error/404.html', status=404)

def handler400(request, exception):
    return render(request, 'error/400.html', status=400)

def handler500(request):
    return render(request, 'error/500.html', status=500)
import logging
import os
import time

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from .forms import (
    AutaForm, MiastaForm, UzytkownicyForm, WypozyczenieForm,
    AdminForm, CzarnaListaForm, LoginForm
)
from .models import Admin, Uzytkownicy, Auta, Miasta, Wypozyczenie, CzarnaLista, AutaZdj


logger = logging.getLogger(__name__)

def index_view(request):
    return render(request, 'index.html')

def admin_dashboard(request):
    if request.session.get('user_type') != 'admin':
        return redirect('login')

    print(f"Trying to render template: admin_dashboard.html")
    return render(request, 'admin-dashboard.html')

def user_dashboard(request):
    """
    User dashboard view displaying available cars
    Redirect to ban info if user is blacklisted
    """
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    user_id = request.session.get('user_id')
    
    # Check if user is on blacklist
    user_ban = CzarnaLista.objects.filter(id_user=user_id, data_koncowa__gte=datetime.now().date()).first()
    if user_ban:
        return redirect('user_ban_info')
    
    # Get all cars with availability information
    all_cars = Auta.objects.all()
    
    # For each car, check if it's currently rented and get the first photo
    cars_with_status = []
    for car in all_cars:
        # Check if car is currently rented
        is_rented = Wypozyczenie.objects.filter(
            id_auta=car,
            data_poczatkowa__lte=datetime.now().date(),
            data_koncowa__gte=datetime.now().date()
        ).exists()
        
        # Get the first photo for this car
        first_photo = AutaZdj.objects.filter(id_auta=car).order_by('kolejnosc').first()
        
        cars_with_status.append({
            'car': car,
            'available': not is_rented,
            'photo': first_photo
        })
    
    return render(request, 'user_dashboard.html', {'cars': cars_with_status})


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
                    from django.contrib.auth.hashers import check_password
                    direct_result = check_password(password, admin.password)
                    logger.info(f"Bezpośrednie sprawdzenie hasła: {direct_result}")

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
                    user = Uzytkownicy.objects.filter(email=email).first()
                    if user:
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

#sprawdzenie sesji admina
def is_admin_logged_in(requst):
    return requst.session.get('user_type') == 'admin' and requst.session.get('user_id')

#sprawdzanie sesji user
def is_user_logged_in(requst):
    return requst.session.get('user_type') == 'user' and requst.session.get('user_id')

#wylogowanie 
def logout_view(requst):
    if 'user_type' in requst.session:
        del requst.session['user_type']

    if 'user_id' in requst.session:
        del requst.session['user_id']

    messages.success('Zostałeś wylogowany')

#Funckje zarządzania autami
def admin_car_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    auta = Auta.objects.all()
    form = AutaForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = AutaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Auto zostało dodane.')
                return redirect('admin_car_view')
        elif 'usun' in request.POST:
            id_auta = request.POST.get('id_auta')
            auto = get_object_or_404(Auta, id_auta=id_auta)
            auto.delete()
            messages.success(request, 'Auto zostało usunięte.')
            return redirect('admin_car_view')
        elif 'edytuj' in request.POST:
            id_auta = request.POST.get('id_auta')
            auto = get_object_or_404(Auta, id_auta=id_auta)
            form = AutaForm(request.POST, instance=auto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Auto zostało zaktualizowane.')
                return redirect('admin_car_view')
    
    return render(request, 'admin_car_view.html', {'auta': auta, 'form': form})

# Funkcje zarządzania adresami zamieszkania
def admin_address_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    miasta = Miasta.objects.all()
    form = MiastaForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = MiastaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Adres został dodany.')
                return redirect('admin_address_view')
        elif 'usun' in request.POST:
            id_zamieszkania = request.POST.get('id_zamieszkania')
            miasto = get_object_or_404(Miasta, id_zamieszkania=id_zamieszkania)
            miasto.delete()
            messages.success(request, 'Adres został usunięty.')
            return redirect('admin_address_view')
        elif 'edytuj' in request.POST:
            id_zamieszkania = request.POST.get('id_zamieszkania')
            miasto = get_object_or_404(Miasta, id_zamieszkania=id_zamieszkania)
            form = MiastaForm(request.POST, instance=miasto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Adres został zaktualizowany.')
                return redirect('admin_address_view')
    
    return render(request, 'admin_address_view.html', {'miasta': miasta, 'form': form})

# Funkcje zarządzania wypożyczeniami
def admin_rent_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    wypozyczenia = Wypozyczenie.objects.all()
    form = WypozyczenieForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = WypozyczenieForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Wypożyczenie zostało dodane.')
                return redirect('admin_rent_view')
        elif 'usun' in request.POST:
            id_wypozyczenia = request.POST.get('id_wypozyczenia')
            wypozyczenie = get_object_or_404(Wypozyczenie, id_wypozyczenia=id_wypozyczenia)
            wypozyczenie.delete()
            messages.success(request, 'Wypożyczenie zostało usunięte.')
            return redirect('admin_rent_view')
        elif 'edytuj' in request.POST:
            id_wypozyczenia = request.POST.get('id_wypozyczenia')
            wypozyczenie = get_object_or_404(Wypozyczenie, id_wypozyczenia=id_wypozyczenia)
            form = WypozyczenieForm(request.POST, instance=wypozyczenie)
            if form.is_valid():
                form.save()
                messages.success(request, 'Wypożyczenie zostało zaktualizowane.')
                return redirect('admin_rent_view')
    
    return render(request, 'admin_rent_view.html', {'wypozyczenia': wypozyczenia, 'form': form})

# Funkcje zarządzania administratorami
def admin_admin_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    administratorzy = Admin.objects.all()
    form = AdminForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = AdminForm(request.POST)
            if form.is_valid():
                admin = form.save(commit=False)
                admin.password = make_password(form.cleaned_data['password'])
                admin.save()
                messages.success(request, 'Administrator został dodany.')
                return redirect('admin_admin_view')
        elif 'usun' in request.POST:
            id_admin = request.POST.get('id_admin')
            # Nie pozwól usunąć zalogowanego administratora
            if int(id_admin) == request.session.get('user_id'):
                messages.error(request, 'Nie możesz usunąć swojego konta!')
                return redirect('admin_admin_view')
                
            admin = get_object_or_404(Admin, id_admin=id_admin)
            admin.delete()
            messages.success(request, 'Administrator został usunięty.')
            return redirect('admin_admin_view')
        elif 'edytuj' in request.POST:
            id_admin = request.POST.get('id_admin')
            admin = get_object_or_404(Admin, id_admin=id_admin)
            form = AdminForm(request.POST, instance=admin)
            if form.is_valid():
                admin = form.save(commit=False)
                if form.cleaned_data.get('password'):
                    admin.password = make_password(form.cleaned_data['password'])
                admin.save()
                messages.success(request, 'Administrator został zaktualizowany.')
                return redirect('admin_admin_view')
    
    return render(request, 'admin_admin_view.html', {'administratorzy': administratorzy, 'form': form})

# Funkcje zarządzania użytkownikami
def admin_user_view(request):
    uzytkownicy = Uzytkownicy.objects.all()
    print(f"Liczba użytkowników: {uzytkownicy.count()}")
    for user in uzytkownicy:
        print(f"ID: {user.id_user}, Imię: {user.imie}, Nazwisko: {user.nazwisko}")
    
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    uzytkownicy = Uzytkownicy.objects.all()
    form = UzytkownicyForm()
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = UzytkownicyForm(request.POST)
            if form.is_valid():
                uzytkownik = form.save(commit=False)
                uzytkownik.haslo = make_password(form.cleaned_data['haslo'])
                uzytkownik.save()
                messages.success(request, 'Użytkownik został dodany.')
                return redirect('admin_user_view')
        elif 'usun' in request.POST:
            id_user = request.POST.get('id_user')
            uzytkownik = get_object_or_404(Uzytkownicy, id_user=id_user)
            uzytkownik.delete()
            messages.success(request, 'Użytkownik został usunięty.')
            return redirect('admin_user_view')
        elif 'edytuj' in request.POST:
            id_user = request.POST.get('id_user')
            uzytkownik = get_object_or_404(Uzytkownicy, id_user=id_user)
            form = UzytkownicyForm(request.POST, instance=uzytkownik)
            if form.is_valid():
                uzytkownik = form.save(commit=False)
                if form.cleaned_data.get('haslo'):
                    uzytkownik.haslo = make_password(form.cleaned_data['haslo'])
                uzytkownik.save()
                messages.success(request, 'Użytkownik został zaktualizowany.')
                return redirect('admin_user_view')
    
    return render(request, 'admin_user_view.html', {'uzytkownicy': uzytkownicy, 'form': form})

# Funkcje zarządzania czarną listą
def admin_blackList_view(request):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    czarna_lista = CzarnaLista.objects.all()
    form = CzarnaListaForm()
    
    # Automatycznie ustaw aktualnego administratora jako dodającego
    if request.method == 'GET':
        try:
            admin_id = request.session.get('user_id')
            admin = Admin.objects.get(id_admin=admin_id)
            form = CzarnaListaForm(initial={'id_admin': admin})
        except Admin.DoesNotExist:
            pass
    
    if request.method == 'POST':
        if 'dodaj' in request.POST:
            form = CzarnaListaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Użytkownik został dodany do czarnej listy.')
                return redirect('admin_blackList_view')
        elif 'usun' in request.POST:
            id_bl = request.POST.get('id_bl')
            wpis = get_object_or_404(CzarnaLista, id_bl=id_bl)
            wpis.delete()
            messages.success(request, 'Wpis został usunięty z czarnej listy.')
            return redirect('admin_blackList_view')
        elif 'edytuj' in request.POST:
            id_bl = request.POST.get('id_bl')
            wpis = get_object_or_404(CzarnaLista, id_bl=id_bl)
            form = CzarnaListaForm(request.POST, instance=wpis)
            if form.is_valid():
                form.save()
                messages.success(request, 'Wpis czarnej listy został zaktualizowany.')
                return redirect('admin_blackList_view')
    
    return render(request, 'admin_blackList_view.html', {'czarna_lista': czarna_lista, 'form': form})

def car_detail(request, car_id):
    """
    Detailed view for a specific car
    """
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    user_id = request.session.get('user_id')
    
    # Check if user is on blacklist
    user_ban = CzarnaLista.objects.filter(id_user=user_id, data_koncowa__gte=datetime.now().date()).first()
    if user_ban:
        return redirect('user_ban_info')
    
    car = get_object_or_404(Auta, id_auta=car_id)
    
    # Get all photos for this car
    car_photos = AutaZdj.objects.filter(id_auta=car).order_by('kolejnosc')
    
    # Check if car is currently rented
    is_rented = Wypozyczenie.objects.filter(
        id_auta=car,
        data_poczatkowa__lte=datetime.now().date(),
        data_koncowa__gte=datetime.now().date()
    ).exists()
    
    # Get rental history for this car
    rental_history = Wypozyczenie.objects.filter(
        id_auta=car
    ).order_by('-data_poczatkowa')
    
    context = {
        'car': car,
        'car_photos': car_photos,
        'available': not is_rented,
        'rental_history': rental_history,
        'today': datetime.now().date()
    }
    
    return render(request, 'car_detail.html', context)

def user_ban_info(request):
    """
    View for displaying ban information
    """
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    user_id = request.session.get('user_id')
    user = get_object_or_404(Uzytkownicy, id_user=user_id)
    
    # Get active bans for this user
    active_ban = CzarnaLista.objects.filter(
        id_user=user_id,
        data_koncowa__gte=datetime.now().date()
    ).first()
    
    if not active_ban:
        # If no active ban, redirect to dashboard
        return redirect('user_dashboard')
    
    context = {
        'user': user,
        'ban': active_ban
    }
    
    return render(request, 'user_ban_info.html', context)

def rent_car(request, car_id):
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    user_id = request.session.get('user_id')
    
    user_ban = CzarnaLista.objects.filter(id_user=user_id, data_koncowa__gte=datetime.now().date()).first()
    if user_ban:
        return redirect('user_ban_info')
    
    car = get_object_or_404(Auta, id_auta=car_id)
    
    is_rented = Wypozyczenie.objects.filter(
        id_auta=car,
        data_poczatkowa__lte=datetime.now().date(),
        data_koncowa__gte=datetime.now().date()
    ).exists()
    
    if is_rented:
        messages.error(request, 'To auto jest obecnie niedostępne.')
        return redirect('car_detail', car_id=car_id)
    
    if request.method == 'POST':
        form = WypozyczenieForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.id_auta = car
            rental.id_user_id = user_id 
            rental.save()
            messages.success(request, 'Auto zostało wypożyczone.')
            return redirect('user_dashboard')
    else:
        initial_data = {
            'id_auta': car,
            'id_user': user_id,
            'data_poczatkowa': datetime.now().date()
        }
        form = WypozyczenieForm(initial=initial_data)
    
    context = {
        'car': car,
        'form': form
    }
    
    return render(request, 'rent_car.html', context)

def admin_car_photos(request, car_id):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    car = get_object_or_404(Auta, id_auta=car_id)
    photos = AutaZdj.objects.filter(id_auta=car).order_by('kolejnosc')
    
    # Pobierz listę dostępnych zdjęć z katalogu
    available_images = []
    cars_dir = os.path.join(settings.MEDIA_ROOT, 'cars')
    if os.path.exists(cars_dir):
        available_images = [f for f in os.listdir(cars_dir) if os.path.isfile(os.path.join(cars_dir, f))]
    
    if request.method == 'POST':
        if 'add_photo' in request.POST:
            selected_image = request.POST.get('selected_image')
            if selected_image:
                # Sprawdź limit zdjęć
                if photos.count() >= 5:
                    messages.error(request, 'Maksymalna liczba zdjęć dla jednego auta to 5.')
                else:
                    # Dodaj nowe zdjęcie do bazy z wybranym plikiem
                    new_photo = AutaZdj(
                        id_auta=car,
                        zdj=f'cars/{selected_image}',  # Ścieżka względna
                        kolejnosc=photos.count() + 1 if photos else 1,
                        created_at=datetime.now()
                    )
                    new_photo.save()
                    messages.success(request, 'Zdjęcie zostało dodane.')
            else:
                messages.error(request, 'Nie wybrano zdjęcia.')
        # reszta kodu funkcji pozostaje bez zmian
    
    context = {
        'car': car,
        'photos': photos,
        'available_images': available_images
    }
    
    return render(request, 'admin_car_photos.html', context)

def admin_car_detail(request, car_id):
    if not is_admin_logged_in(request):
        messages.error(request, 'Musisz być zalogowany jako administrator.')
        return redirect('login')
    
    car = get_object_or_404(Auta, id_auta=car_id)
    photos = AutaZdj.objects.filter(id_auta=car).order_by('kolejnosc')
    
    # Obsługa dodawania/usuwania zdjęć
    if request.method == 'POST':
        if 'add_photo' in request.POST:
            if 'photo' in request.FILES:
                # Sprawdź limit zdjęć
                if photos.count() >= 5:
                    messages.error(request, 'Maksymalna liczba zdjęć dla jednego auta to 5.')
                else:
                    # Dodaj nowe zdjęcie
                    new_photo = AutaZdj(
                        id_auta=car,
                        zdj=request.FILES['photo'],
                        kolejnosc=photos.count() + 1 if photos else 1
                    )
                    new_photo.save()
                    messages.success(request, 'Zdjęcie zostało dodane.')
            else:
                messages.error(request, 'Nie wybrano pliku.')
                
        elif 'delete_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            photo = get_object_or_404(AutaZdj, id_zdj=photo_id, id_auta=car)
            photo.delete()
            
            # Aktualizacja kolejności pozostałych zdjęć
            remaining_photos = AutaZdj.objects.filter(id_auta=car).order_by('kolejnosc')
            for i, p in enumerate(remaining_photos, 1):
                p.kolejnosc = i
                p.save()
                
            messages.success(request, 'Zdjęcie zostało usunięte.')
        
        # Odświeżamy listę zdjęć po operacjach
        photos = AutaZdj.objects.filter(id_auta=car).order_by('kolejnosc')
    
    # Dla formularza edycji auta
    if request.method == 'POST' and 'edit_car' in request.POST:
        form = AutaForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Auto zostało zaktualizowane.')
    else:
        form = AutaForm(instance=car)
    
    context = {
        'car': car,
        'photos': photos,
        'form': form,
        'active_tab': request.GET.get('tab', 'info')  # Domyślnie aktywna zakładka 'info'
    }
    
    return render(request, 'admin_car_detail.html', context)

def handler404(request,exeption):
    return render(request, '404.html', status=404)

def handler400(request, exception):
    return render(request, '400.html', status=400)

def handler500(request):
    return render(request, '500.html', status=500)
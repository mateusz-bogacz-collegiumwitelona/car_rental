from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Admin, Uzytkownicy

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Sprawdź admina
            admin = Admin.objects.filter(email=email).first()
            if admin and admin.check_password(password):
                request.session['user_type'] = 'admin'
                request.session['user_id'] = admin.id_admin
                return redirect('admin_dashboard')
            
            # Sprawdź użytkownika
            user = Uzytkownicy.objects.filter(email=email).first()
            if user and user.check_password(password):
                request.session['user_type'] = 'user'
                request.session['user_id'] = user.id_user
                return redirect('user_dashboard')
            
            messages.error(request, 'Nieprawidłowy email lub hasło')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def admin_dashboard(request):
    if request.session.get('user_type') != 'admin':
        return redirect('login')
    
    admin_id = request.session.get('user_id')
    admin = Admin.objects.get(id_admin=admin_id)
    return render(request, 'admin_dashboard.html', {'admin': admin})

def user_dashboard(request):
    if request.session.get('user_type') != 'user':
        return redirect('login')
    
    user_id = request.session.get('user_id')
    user = Uzytkownicy.objects.get(id_user=user_id)
    return render(request, 'user_dashboard.html', {'user': user})

def logout_view(request):
    request.session.flush()
    return redirect('login')
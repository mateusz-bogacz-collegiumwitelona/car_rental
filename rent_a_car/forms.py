from django import forms
from .models import Admin, Auta, Miasta, Uzytkownicy, Wypozyczenie, CzarnaLista
#logowanie 
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Wprowadź email'
        })
    )
    password = forms.CharField(
        label='Hasło', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Wprowadź hasło'
        })
    )

#formularz auta
class CarForm(forms.ModelForm):
    class Meta:
        model = Auta
        fields = ['marka', 'model', 'rocznik', 'opis', 'osiagi']

        widgets = {
            'marka': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'rocznik': forms.NumberInput(attrs={'class': 'form-control'}),
            'opis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'osiagi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        labels = {
            'marka': 'Marka',
            'model': 'Model',
            'rocznik': 'Rocznik',
            'opis': 'Opis',
            'osiagi': 'Osiągi',
        }


#folmularz miasta
class CityForm(forms.ModelForm):
    class Meta:
        model = Miasta
        fields = ['miasto', 'ulica', 'nr_ulicy', 'kod_pocztowy']

        widgets = {
            'miasto': forms.TextInput(attrs={'class': 'form-control'}),
            'ulica': forms.TextInput(attrs={'class': 'form-control'}),
            'nr_ulicy': forms.TextInput(attrs={'class': 'form-control'}),
            'kod_pocztowy': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00-000'}),
        }

        labels = {
            'miasto': 'Miasto',
            'ulica': 'Ulica',
            'nr_ulicy': 'Numer ulicy',
            'kod_pocztowy': 'Kod pocztowy',
        }

#folmularz urzytkowicy
class UserForm(forms.ModelForm):
    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={'class': 'form_control'}),
        required=False
    )

    check_password = forms.CharField(
        label='Potwierdź Hasło',
        widget=forms.PasswordInput(attrs={'class': 'form_control'}),
        required=False
    )

    class Meta:
        model = Uzytkownicy
        fields = ['imie', 'nazwisko', 'pesel', 'email', 'id_zamieszkania']
        widgets = {
            'imie': forms.TextInput(attrs={'class': 'form-control'}),
            'nazwisko': forms.TextInput(attrs={'class': 'form-control'}),
            'pesel': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'id_zamieszkania': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'imie': 'Imię',
            'nazwisko': 'Nazwisko',
            'pesel': 'PESEL',
            'email': 'Email',
            'id_zamieszkania': 'Adres zamieszkania',
        }

    def clean(self):
        cleaned_data = super().clean()
        passwrod = cleaned_data.get('haslo')
        check_password = cleaned_data.get('potwierdzenie_hasla')

        if passwrod and passwrod != check_password:
            raise forms.ValidationError("Hasła nie są idętyczne")
        
        return cleaned_data
    
#formularz admina
class AdminForm(forms.ModelForm):
    password = forms.CharField(
        label='Hasło', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    check_password = forms.CharField(
        label='Potwierdź hasło', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Admin
        fields = ['imie', 'nazwisko', 'email']
        widgets = {
            'imie': forms.TextInput(attrs={'class': 'form-control'}),
            'nazwisko': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'imie': 'Imię',
            'nazwisko': 'Nazwisko',
            'email': 'Email',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        check_password = cleaned_data.get('potwierdzenie_hasla')

        if password and password != check_password:
            raise forms.ValidationError("Hasła nie są identyczne.")
        
        return cleaned_data

#formularz wypożyczenia
class RentForm(forms.ModelForm):
    class Meta:
        model = Wypozyczenie
        fields = ['data_poczatkowa', 'data_koncowa', 'id_auta', 'id_user']
        widgets = {
            'data_poczatkowa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_koncowa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_auta': forms.Select(attrs={'class': 'form-control'}),
            'id_user': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'data_poczatkowa': 'Data początkowa',
            'data_koncowa': 'Data końcowa',
            'id_auta': 'Auto',
            'id_user': 'Użytkownik',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_data = cleaned_data.get('data_poczatkowa')
        end_data = cleaned_data.get('data_koncowa')

        if start_data and end_data and start_data > end_data:
            raise forms.ValidationError("Data początkowa nie może być późniejsza niż data końcowa.")
        
        return cleaned_data

#formalrz czarnej listy
class BlackListForm(forms.ModelForm):
    class Meta:
        model = CzarnaLista
        fields = ['id_user', 'powod', 'data_poczatkowa', 'data_koncowa', 'id_admin']
        widgets = {
            'id_user': forms.Select(attrs={'class': 'form-control'}),
            'powod': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'data_poczatkowa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_koncowa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_admin': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'id_user': 'Użytkownik',
            'powod': 'Powód',
            'data_poczatkowa': 'Data początkowa',
            'data_koncowa': 'Data końcowa',
            'id_admin': 'Administrator',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_data = cleaned_data.get('data_poczatkowa')
        end_data = cleaned_data.get('data_koncowa')

        if start_data and end_data and start_data > end_data:
            raise forms.ValidationError("Data początkowa nie może być późniejsza niż data końcowa.")
        
        return cleaned_data
    

class RegistrationForm(forms.ModelForm):
    # Pola użytkownika
    password = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    check_passowrd = forms.CharField(
        label='Potwierdź Hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    # Pola adresowe
    city = forms.CharField(
        label='Miasto',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    street = forms.CharField(
        label='Ulica',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    street_numb = forms.CharField(
        label='Numer ulicy',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    zip_code = forms.CharField(
        label='Kod pocztowy',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00-000'}),
        required=True
    )

    class Meta:
        model = Uzytkownicy
        fields = ['imie', 'nazwisko', 'pesel', 'email']
        widgets = {
            'imie': forms.TextInput(attrs={'class': 'form-control'}),
            'nazwisko': forms.TextInput(attrs={'class': 'form-control'}),
            'pesel': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'imie': 'Imię',
            'nazwisko': 'Nazwisko',
            'pesel': 'PESEL',
            'email': 'Email',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('haslo')
        check_password = cleaned_data.get('potwierdzenie_hasla')

        if password and password != check_password:
            raise forms.ValidationError("Hasła nie są identyczne")
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Uzytkownicy.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten adres email jest już używany")
        return email
    
    def clean_kod_pocztowy(self):
        zip_code = self.cleaned_data.get('kod_pocztowy')
        # Sprawdź, czy kod pocztowy jest w formacie XX-XXX
        import re
        if not re.match(r'^\d{2}-\d{3}$', zip_code):
            raise forms.ValidationError("Kod pocztowy powinien być w formacie XX-XXX")
        return zip_code
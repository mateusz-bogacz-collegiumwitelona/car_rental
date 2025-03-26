from django import forms

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

from django.shortcuts import render
from .models import Users, City

def user_list(request):
    users = Users.objects.select_related('id_city').all()
    return render(request, 'users/user_list.html', {'users':users})
                  
def user_details(request, id_user):
    users = Users.objects.select_related('id_city').get(id_user=id_user)
    return render(request, 'users/user_details.html', {'users':users})
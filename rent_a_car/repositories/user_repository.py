from ..models import Uzytkownicy, Miasta

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return Uzytkownicy.objects,filter(id_user=user_id).first()
    
    @staticmethod
    def get_by_email(email):
        return Uzytkownicy.objects.filter(email=email).first()
    
    @staticmethod
    def create_user(user_data):
        user = Uzytkownicy(**user_data)
        user.save()
        return user
    
    @staticmethod
    def create_address(address_data):
        address = Miasta(**address_data)
        address.save
        return address
    
    @staticmethod 
    def update_user(user):
        user.save()
        return user
    
    @staticmethod
    def delete_user(user_id):
        user = Uzytkownicy.objects.get(id_user=user_id)
        user.delete()

    @staticmethod
    def fet_all_users():
        return Uzytkownicy.objects.all()
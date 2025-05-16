from ..models import Uzytkownicy, Miasta

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return Uzytkownicy.objects.filter(id_user=user_id).first()
    
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
        address.save()
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
    def get_all_users(): 
        return Uzytkownicy.objects.all()
    
    @staticmethod
    def delete_addresses(address_id):
        address = Miasta.objects.get(id_zamieszkania=address_id)
        address.delete()
        return True
    
    @staticmethod
    def update_address(address_id, address_data):
        address = Miasta.objects.get(id_zamieszkania=address_id)
        for key, value in address_data.items():
            setattr(address, key, value)
        address.save()
        return address
    
    @staticmethod
    def get_address_by_id(address_id):
        return Miasta.objects.filter(id_zamieszkania=address_id).first()
    
    @staticmethod
    def check_email_exists(email, exclude_user_id=None):
        query = Uzytkownicy.objects.filter(email=email)
        if exclude_user_id:
            query = query.exclude(id_user=exclude_user_id)
        return query.exists()
    
    @staticmethod
    def check_pesel_exists(pesel, exclude_user_id=None):
        query = Uzytkownicy.objects.filter(pesel=pesel)
        if exclude_user_id:
            query = query.exclude(id_user=exclude_user_id)
        return query.exists()
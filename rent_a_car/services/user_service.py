from django.contrib.auth.hashers import make_password, check_password
from ..repositories.user_repository import UserRepository
from ..repositories.blacklist_repository import BlacklistRepository
from ..models import Miasta

class UserService:
    @staticmethod
    def create_user(user_data, address_data):
        if UserRepository.check_email_exists(user_data['email']):
            raise ValueError("Ten adres email jest już używany przez innego użytkownika")

        if UserRepository.check_pesel_exists(user_data['pesel']):
            raise ValueError("Ten numer PESEL jest już używany przez innego użytkownika")
        
        address = UserRepository.create_address(address_data)
        
        user_data['haslo'] = make_password(user_data['haslo'])
        user_data['id_zamieszkania'] = address

        user = UserRepository.create_user(user_data)
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.get_by_email(email)

        if user and check_password(password, user.haslo):
            return user
        
        return None
    
    @staticmethod
    def is_blacklisted(user_id, current_data=None):
        return BlacklistRepository.is_user_blacklisted(user_id, current_data)
    
    @staticmethod
    def get_active_ban(user_id, current_data=None):
        return BlacklistRepository.get_active_ban(user_id, current_data)
    
    @staticmethod
    def update_user(user_id, user_data, password=None):
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return None

        if 'email' in user_data and user_data['email'] != user.email:
            if UserRepository.check_email_exists(user_data['email'], exclude_user_id=user_id):
                raise ValueError("Ten adres email jest już używany przez innego użytkownika")
        
        if 'pesel' in user_data and user_data['pesel'] != user.pesel:
            if UserRepository.check_pesel_exists(user_data['pesel'], exclude_user_id=user_id):
                raise ValueError("Ten numer PESEL jest już używany przez innego użytkownika")

        for key, value in user_data.items():
            setattr(user, key, value)

        if password:
            user.haslo = make_password(password)
        
        UserRepository.update_user(user)
        return user
    
    @staticmethod
    def get_all_users():
        return list(UserRepository.get_all_users())
    
    @staticmethod
    def get_all_addresses():
        return Miasta.objects.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_by_id(user_id)
    
    @staticmethod
    def create_address(address_data):
        return UserRepository.create_address(address_data)
    
    @staticmethod
    def delete_address(address_id):
        return UserRepository.delete_addresses(address_id)
    
    @staticmethod
    def update_address(address_id, address_data):
        return UserRepository.update_address(address_id, address_data)
    
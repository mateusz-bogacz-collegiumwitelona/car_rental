from django.contrib.auth.hashers import make_password, check_password
from ..repositories.user_repository import UserRepository
from ..repositories.blacklist_repository import BlacklistRepository

class UserService:
    @staticmethod
    def create_user(user_data, address_data):
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
        
        for key, value in user_data.items():
            setattr(user, key, value)

        if password:
            user.haslo = make_password(password)
        
        UserRepository.update_user(user)

        return user
    
    @staticmethod
    def get_all_users():
        return list(UserRepository.get_all_users())
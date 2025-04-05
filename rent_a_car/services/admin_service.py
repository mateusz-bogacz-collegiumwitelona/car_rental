from django.contrib.auth.hashers import make_password, check_password
from ..repositories.admin_repository import AdminRepository

class AdminService:
    @staticmethod
    def get_admin_by_id(admin_id):
        return AdminRepository.get_by_id(admin_id)


    @staticmethod
    def authenticate_admin(email, password):
        admin = AdminRepository.get_by_email(email)
        
        if admin and check_password(password, admin.password):
            return admin
        
        return None
    
    @staticmethod
    def create_admin(admnin_data, password):
        admnin_data['password'] = make_password(password)
        return AdminRepository.create_admin(admnin_data)
    
    def update_admin(admin_id, admin_data, password=None):
        admin = AdminRepository.get_by_id(admin_id)

        if not admin:
            return None
        
        for key, value in admin_data.items():
            setattr(admin, key, value)

        if password:
            admin.password = make_password(password)

        AdminRepository.update_admin(admin)
        return admin
    
    @staticmethod
    def get_all_admins():
        return AdminRepository.get_all_admins()
    
    @staticmethod
    def delete_admin(admin_id):
        return AdminRepository.delete_admin(admin_id)
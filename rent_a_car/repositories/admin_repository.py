from ..models import Admin
from ..repositories.admin_repository import AdminRepository

class AdminRepository:
    @staticmethod
    def get_by_id(admin_id):
        return Admin.objects.filter(id_admin=admin_id).first()
    
    @staticmethod
    def get_by_email(email):  # Make sure parameter is named 'email', not 'emial'
        return Admin.objects.filter(email=email).first()
    
    @staticmethod
    def get_all_admins():
        return Admin.objects.all()
    
    @staticmethod
    def create_admin(admin_data):
        admin = Admin(**admin_data)
        admin.save()
        return admin
    
    @staticmethod
    def update_admin(admin):
        admin.save()
        return admin
    
    @staticmethod
    def delete_admin(admin_id):
        admin = Admin.objects.get(id_admin=admin_id)
        admin.delete()

    @staticmethod 
    def get_admin_by_id(admin_id):
        return AdminRepository.get_by_id(admin_id)
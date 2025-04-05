from ..models import CzarnaLista
from datetime import datetime

class BlacklistRepository:
    @staticmethod
    def get_all_blacklist_entries():
        return CzarnaLista.objects.all()
    
    @staticmethod
    def is_user_blacklisted(user_id, date=None):
        if date is None:
            date = datetime.now().date()

        return CzarnaLista.objects.filter(
            id_user_id=user_id,
            data_koncowa__gte=date
        ).exists()
    
    @staticmethod
    def get_active_ban(user_id, date=None):
        if date is None:
            date = datetime.now().date()

        return CzarnaLista.objects.filter(
            id_user_id=user_id,
            data_koncowa__gte=date
        ).first()
    
    @staticmethod
    def create_blacklist_entry(blacklist_data):
        entry = CzarnaLista(**blacklist_data)
        entry.save()
        return entry
    
    @staticmethod
    def delete_blacklist_entry(blacklist_id):
        entry = CzarnaLista.objects.get(id_bl=blacklist_id)
        entry.delete()
        return True
    
    @staticmethod
    def update_blacklist_entry(blacklist_id, blacklist_data):
        entry = CzarnaLista.objects.get(id_bl=blacklist_id)
        for key, value in blacklist_data.items():
            setattr(entry, key, value)
        entry.save()
        return entry
        
    @staticmethod
    def get_blacklist_entry_by_id(blacklist_id):
        return CzarnaLista.objects.filter(id_bl=blacklist_id).first()
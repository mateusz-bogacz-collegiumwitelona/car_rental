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
    
    def create_blacklist_entry(blacklist_data):
        entry = CzarnaLista(**blacklist_data)
        entry.save()
        return entry
    
    

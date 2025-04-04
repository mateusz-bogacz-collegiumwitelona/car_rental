from ..repositories.blacklist_repository import BlacklistRepository

class BlacklistService:
    @staticmethod
    def add_to_blacklist(blacklist_data):
        return BlacklistRepository.create_blacklist_entry(blacklist_data)
    
    @staticmethod
    def get_all_blacklist():
        return BlacklistRepository.get_all_blacklist_entries()
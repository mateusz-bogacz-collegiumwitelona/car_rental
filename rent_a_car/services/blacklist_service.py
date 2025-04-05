from ..repositories.blacklist_repository import BlacklistRepository

class BlacklistService:
    @staticmethod
    def add_to_blacklist(blacklist_data):
        return BlacklistRepository.create_blacklist_entry(blacklist_data)
    
    @staticmethod
    def get_all_blacklist():
        return BlacklistRepository.get_all_blacklist_entries()
    
    @staticmethod
    def delete_blacklist_entry(blacklist_id):
        return BlacklistRepository.delete_blacklist_entry(blacklist_id)

    @staticmethod
    def update_blacklist_entry(blacklist_id, blacklist_data):
        return BlacklistRepository.update_blacklist_entry(blacklist_id, blacklist_data)

    @staticmethod
    def get_blacklist_entry_by_id(blacklist_id):
        return BlacklistRepository.get_blacklist_entry_by_id(blacklist_id)
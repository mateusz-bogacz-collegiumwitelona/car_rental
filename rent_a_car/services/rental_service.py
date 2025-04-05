from ..repositories.rental_repository import RentalRepository
from ..repositories.car_repository import CarRepository
from ..repositories.user_repository import UserRepository
from ..repositories.blacklist_repository import BlacklistRepository

class RentalService:
    @staticmethod
    def create_rental(rental_data):
        car_id = rental_data.get('id_auta_id') or rental_data.get('id_auta').id_auta
        user_id = rental_data.get('id_user_id') or rental_data.get('id_user').id_user

        from datetime import datetime
        start_data = rental_data.get('data_poczatkowa')

        if BlacklistRepository.is_user_blacklisted(user_id, start_data):
            return None, 'Użytkownik nie jest na czarnej liście'
        
        if RentalRepository.get_active_rentals_for_car(car_id, start_data).exists():
            return None, 'Auto nie jest dostępne w tym terminie'
        
        return RentalRepository.create_rental(rental_data), None
    
    @staticmethod
    def get_all_rentals():
        return RentalRepository.get_all_rentals()
    
    @staticmethod
    def delete_rental(rental_id):
        return RentalRepository.delete_rental(rental_id)

    @staticmethod
    def update_rental(rental_id, rental_data):
        return RentalRepository.update_rental(rental_id, rental_data)

    @staticmethod
    def get_rental_by_id(rental_id):
        return RentalRepository.get_rental_by_id(rental_id)
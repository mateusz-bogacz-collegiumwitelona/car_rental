from ..models import Wypozyczenie
from datetime import datetime

class RentalRepository:
    @staticmethod
    def get_all_rentals():
        return Wypozyczenie.objects.all()
    
    @staticmethod
    def create_rental(rental_data):
        rental = Wypozyczenie(**rental_data)
        rental.save()
        return rental
    
    @staticmethod
    def get_active_rentals_for_car(car_id, date=None):
        if date is None:
            date = datetime.now().date()
        
        return Wypozyczenie.objects.filter(
            id_auta_id=car_id,
            data_poczatkowa__lte=date,
            data_koncowa__gte=date
        )
    
    @staticmethod
    def get_rental_history_for_car(car_id):
        return Wypozyczenie.objects.filter(id_auta_id=car_id).order_by('-data_poczatkowa')

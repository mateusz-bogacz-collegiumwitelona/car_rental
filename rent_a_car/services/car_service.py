from ..repositories.car_repository import CarRepository
from ..repositories.rental_repository import RentalRepository
from datetime import datetime
import os
from django.conf import settings
        
class CarService:
    @staticmethod
    def get_car_by_id(car_id):
        return CarRepository.get_car_by_id(car_id)

    @staticmethod
    def get_all_cars_with_status():
        all_cars = CarRepository.get_all_cars()
        cars_with_status = []
        
        for car in all_cars:
            is_rented = RentalRepository.get_active_rentals_for_car(car.id_auta).exists()
            first_photo = CarRepository.get_car_photos(car.id_auta).first()
            
            cars_with_status.append({
                'car': car,
                'available': not is_rented,
                'photo': first_photo
            })
        
        return cars_with_status
    
    @staticmethod
    def update_car(car_id, car_data):
        car = CarRepository.get_car_by_id(car_id)
        if not car:
            return None
        
        for key, value in car_data.items():
            setattr(car, key, value)
        
        return CarRepository.update_car(car)

    @staticmethod
    def is_car_available(car_id, date=None):
        return not RentalRepository.get_active_rentals_for_car(car_id, date).exists()
    
    @staticmethod
    def get_car_details(car_id):
        car = CarRepository.get_car_by_id(car_id)
        if not car:
            return None
        
        photos = CarRepository.get_car_photos(car_id)
        is_rented = not CarService.is_car_available(car_id)
        rental_history = RentalRepository.get_rental_history_for_car(car_id)
        
        return {
            'car': car,
            'photos': photos,
            'available': not is_rented,
            'rental_history': rental_history
        }
    
    @staticmethod
    def add_car_photo(car_id, photo_data):
        from ..repositories.car_repository import CarRepository
        car = CarRepository.get_car_by_id(car_id)
        if not car:
            return None
        
        photo_data['id_auta'] = car
        return CarRepository.add_car_photo(photo_data)

    @staticmethod
    def get_car_photos(car_id):
        return CarRepository.get_car_photos(car_id)

    @staticmethod
    def delete_car_photo(photo_id):
        return CarRepository.delete_car_photo(photo_id)

    @staticmethod
    def get_all_cars():
        return CarRepository.get_all_cars()
    
    @staticmethod
    def get_available_images():
        available_images = []
        cars_dir = os.path.join(settings.MEDIA_ROOT, 'cars')
        os.makedirs(cars_dir, exist_ok=True)
        
        if os.path.exists(cars_dir):
            available_images = [f for f in os.listdir(cars_dir) if os.path.isfile(os.path.join(cars_dir, f)) and 
                               f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        return available_images
    
    @staticmethod
    def create_car(car_data):
        return CarRepository.create_car(car_data)
    
    @staticmethod
    def delete_car(car_id):
        return CarRepository.delete_car(car_id)
    
    @staticmethod
    def update_photo_order(car_id, photo_id, new_order):
        return CarRepository.update_photo_order(car_id, photo_id, new_order)
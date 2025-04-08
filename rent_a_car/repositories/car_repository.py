from ..models import Auta, AutaZdj
import os
from django.conf import settings
from django.db import models

class CarRepository:
    @staticmethod
    def get_all_cars():
        return Auta.objects.all()
    
    @staticmethod
    def get_car_by_id(car_id):
        return Auta.objects.filter(id_auta=car_id).first()
    
    @staticmethod
    def create_car(car_data):
        car = Auta(**car_data)
        car.save()
        return car
    
    @staticmethod
    def update_car(car):
        car.save()
        return car
    
    @staticmethod 
    def get_car_photos(car_id):
        return AutaZdj.objects.filter(id_auta=car_id).order_by('kolejnosc')
    
    @staticmethod
    def add_car_photo(photo_data):
        photo = AutaZdj(**photo_data)
        photo.save()
        return photo
    
    @staticmethod
    def delete_car_photo(photo_id):
        try:
            photo = AutaZdj.objects.get(id_zdj=photo_id)
            file_path = photo.zdj

            if file_path and file_path.startswith('cars/'):
                other_uses = AutaZdj.objects.filter(zdj=file_path).exclude(id_zdj=photo_id).count()
                
                if other_uses == 0:
                    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    
                    if os.path.exists(full_path):
                        try:
                            os.remove(full_path)
                        except (OSError, PermissionError) as e:
                            print(f"Nie można usunąć pliku: {e}")
            
            photo.delete()
            return True
        except AutaZdj.DoesNotExist:
            return False
    
    @staticmethod
    def delete_car(car_id):

        car = Auta.objects.get(id_auta=car_id)
        photos = AutaZdj.objects.filter(id_auta=car_id)
        for photo in photos:
            CarRepository.delete_car_photo(photo.id_zdj)
        
        car.delete()
        return car
        
    @staticmethod
    def update_photo_order(car_id, photo_id, new_order):
        try:
            photo_to_update = AutaZdj.objects.get(id_zdj=photo_id)
            old_order = photo_to_update.kolejnosc
            new_order = int(new_order)
            if old_order == new_order:
                return photo_to_update
            
            if old_order < new_order:
                AutaZdj.objects.filter(
                    id_auta=car_id, 
                    kolejnosc__gt=old_order, 
                    kolejnosc__lte=new_order
                ).update(kolejnosc=models.F('kolejnosc') - 1)
            else:
                AutaZdj.objects.filter(
                    id_auta=car_id, 
                    kolejnosc__lt=old_order, 
                    kolejnosc__gte=new_order
                ).update(kolejnosc=models.F('kolejnosc') + 1)

            photo_to_update.kolejnosc = new_order
            photo_to_update.save()
            
            return photo_to_update
        except AutaZdj.DoesNotExist:
            return None
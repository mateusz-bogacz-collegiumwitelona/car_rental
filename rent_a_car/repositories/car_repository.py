from ..models import Auta, AutaZdj

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
        photo = AutaZdj.objects.get(id_zdj=photo_id)
        photo.delete()
        return True
    
    @staticmethod
    def delete_car(car_id):
        car = Auta.objects.get(id_auta=car_id)
        car.delete()
        return car
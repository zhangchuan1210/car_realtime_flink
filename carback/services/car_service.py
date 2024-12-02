
from extensions import db
from models.car import Car

class CarService:
    def get_car_by_id(self,car_id):
        return db.session.execute("select * from user_t where id=?", car_id)

    def get_all_cars(self):
        page_size=10
        total_count = db.session.query(Car).count()
        all_cars=[]
        for page in (total_count+page_size-1)/page_size:
            cars=db.session.query(Car).limit(page_size).offset((page - 1) * page_size).all()
            all_cars.append(cars)
        return all_cars

    def add_car(self,model, brand, year, price):
        car = Car(model=model, brand=brand, year=year, price=price)
        db.session.add(car)
        db.session.commit()
        return car

    def delete_car(self,car_id):
        car = Car.query.get(car_id)
        if car:
            db.session.delete(car)
            db.session.commit()
        return car

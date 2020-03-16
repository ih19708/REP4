import random
from objects import Lane, Car, Bridge

class BridgeSystem(Bridge):
    ############################
    """THIS IS THE LOGIC BEHIND THE ANIMATION"""
    def init(self):
        for car in self.cars:
            car.speed = 8
            car.status = "waiting"
            if car.direction == -1:
                car.position = (self.rel_length + (car.ID * (car.length / 2)\
                                + 0.4 * (car.ID - 1)), -5)
            else:
                car.position = ((car.ID * (-car.length / 2) - 0.4 * (car.ID - 1)), 5)
        events = []
        return events

    def update(self):
        self.driving_cars = []
        self.passed_cars = []
        

        for car in self.cars:
            if car.status == "passed":
                self.passed_cars.append(car)
            elif car.status == "driving":
                self.driving_cars.append(car)
                
        for car in self.traffic["R"]:
            if car.status == "waiting":
                self.R_waiting_cars.append(car)
                         
        if  self.traffic_flow == 1 and len(self.R_waiting_cars) > 0:
            self.R_waiting_cars[0].status = "driving"
            self.R_waiting_cars.remove(self.R_waiting_cars[0])

            if  self.traffic_flow == - 1 and len(self.L_waiting_cars) > 0:
                print("-1")
                self.L_waiting_cars[0].status = "driving"
                self.R_waiting_cars.remove(self.R_waiting_cars[0])
        
        for car in self.traffic["L"]:
            if car.status == "waiting":
                self.L_waiting_cars.append(car)
                         

        if len(self.passed_cars) - 1 % 2 != 0:
            self.traffic_flow == -1
        else:
            self.traffic_flow == 1


        events = []
        for car in self.cars:
            if car.status == "driving" or car.status == "passed":
                events += self.update_car(car)
        
        return events
    #################################################################
    def update_car(self, car):
        """Update simulation state of car."""

        # Assume all cars have speed 1 (needs to be an int)
        speed = car.speed
        x_0, y_0 = car.position
        x = x_0 + speed * car.direction
        car.position = (x, y_0)

        if car.direction == 1:
            if x_0 > self.rel_length:
                car.status = "passed"
        else:
            if x_0 < 0:
                car.status = "passed"
        events = []
        return events

if __name__ == "__main__":
    import doctest
    doctest.testmod()

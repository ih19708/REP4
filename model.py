import random
from objects import Car, Bridge

class BridgeSystem(Bridge):
    ############################
    """THIS IS THE LOGIC BEHIND THE ANIMATION"""
    def init(self):
        for car in self.cars:
            car.position = car.start_position(self.rel_length, self.bridge_width)
        events = []
        return events

    def update(self):
        events = []

        for car in self.cars:
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
            if x_0 > self.rel_length / 2:
                car.status = "passed"
        else:
            if x_0 < - self.rel_length / 2:
                car.status = "passed"
        events = []
        return events

if __name__ == "__main__":
    import doctest
    doctest.testmod()

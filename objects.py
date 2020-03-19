import matplotlib
from matplotlib.patches import Rectangle
import random

COLOURS = ["b", "r", "g", "w", "m", "c", "y", "maroon", "teal", "gold", "palegreen"
, "indigo", "navy", "salmon", "orange", "silver", "lime", "azure", "mediumvioletred"]
class Printable:
    def __str__(self):
        classname = type(self).__name__
        args = [getattr(self, p) for p in self.parameters]
        return '%s(%s)' % (classname, ', '.join(map(repr, args))) + "\n##########################"

class Car(Printable):
    parameters = "ID", "direction", "speed", "position", "status", "colour"
    def __init__(self, ID, direction, speed, length=1):
        if not isinstance(ID, int):
            raise TypeError('ID should be an integer')
        if direction not in {1, -1}:
            raise TypeError('direction should be 1 or -1')
        if not (isinstance(speed, int)) and speed > 0:
            raise TypeError('speed should be an int and greater than 0')

        self.ID = ID
        self.length = length 
        self.direction = direction
        self.speed = speed

        self.position = (0,0)
        self.colour = random.choice(COLOURS)
        self.width = 0.4 * self.length
        self.buffer = 0.3
        self.go = False
        self.status = ""
    
    def start_position(self, rel_length, bridge_width):
        if self.direction == 1:
            x, y = -((rel_length / 2) + self.buffer * (self.ID - 1)+ self.length * self.ID),\
                bridge_width - self.length / 2
        else:
            x, y = ((rel_length / 2) + self.buffer * (self.ID - 1)+ self.length * self.ID) - 1\
                , 0.5 * (bridge_width - self.length)
        return x, y

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""
        x, y = self.position
        self.car_rect = Rectangle((x, y), self.length, self.width,\
                        facecolor=self.colour, edgecolor="k", zorder=3)
        ax.add_artist(self.car_rect)
        #self.text = ax.text(x, y+3, str(self.ID),
                #verticalalignment='bottom', horizontalalignment='center')
        return [self.car_rect]

    def update_animation(self):
        """Update matplotlib animation for axes ax"""
        # Redraw the car
        x, y = self.position
        #self.car_line.set_data([x], [y])
        self.car_rect.set_xy((x, y))
        # Update text position
        #self.text.set_x(x)
        #self.text.set_y(y+3)
        # Return the patches for matplotlib to update
        return [self.car_rect]

class Bridge():
    def __init__(self, rel_length, cars):
        self.rel_length = rel_length
        self.cars = cars

        #####################################################
        self.traffic = {
            "R" : [car for car in cars if car.direction == 1],
            "L" : [car for car in cars if car.direction == -1]
        }
        #####################################################
        self.start = 0
        self.end = self.start + self.rel_length

        ###########################################
        self.traffic_flow = 1
        self.driving_cars = []
        self.passed_cars = []
        self.R_waiting_cars = []
        self.L_waiting_cars = []
        ##########################################

        """ For animations """
        self.bridge_width = 1.3
        self.bridge_pos = -self.rel_length / 2, 0
        self.road_length = (1/3) * self.rel_length
        self.road_width = 1.5


    def init(self):
        """Initialise the model after creating nand return events"""
        raise NotImplementedError("Subclasses should override this method")

    def update(self):
        """Updates the model through one timestep"""
        raise NotImplementedError("Subclasses should override this method")

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""

        # Initialise self before child objects
        patches = self._init_animation(ax)

        # Initialise all cars
        for car in self.cars:
            patches += car.init_animation(ax)

        # List of patches for matplotlib to update
        return patches

    def update_animation(self):
        """Update matplotlib animation for axes ax"""
        # Redraw cars
        patches = []
        for car in self.cars:
            patches += car.update_animation()

        # List of patches for matplotlib to update
        return patches

    def _init_animation(self, ax):
        """Initialise self for animation in axes ax"""
        xmin, xmax = - self.rel_length / 2 - self.road_length,\
                    self.rel_length / 2 + self.road_length 
        ymin, ymax =  xmin, xmax
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        RIVER_LENGTH = ymax - ymin

        river_width = self.rel_length * 0.85
        river_pos = - 0.5 * river_width, ymin 
        left_road_pos = -self.rel_length / 2 - self.road_length,\
                        - 0.5 * (self.road_width - self.bridge_width)
        right_road_pos = self.rel_length / 2, - 0.5 * (self.road_width - self.bridge_width)

        river = Rectangle((river_pos), river_width, RIVER_LENGTH, color="steelblue",\
                zorder=1)
        Bridge = Rectangle((self.bridge_pos), self.rel_length, self.bridge_width,\
                facecolor="dimgray", edgecolor="k", zorder=2) 
        right_road = Rectangle((right_road_pos), self.road_length , self.road_width,\
                    color="k", zorder=2)
        left_road = Rectangle(left_road_pos, self.road_length, self.road_width,\
                    color="k", zorder=2)

        ax.add_artist(river)
        ax.add_artist(Bridge)
        ax.add_artist(left_road)
        ax.add_artist(right_road)

        x1 = [xmin, 0 - self.rel_length / 2]
        x2 = [self.rel_length / 2, xmax]
        y = [0.5 * self.bridge_width, self.bridge_width / 2]

        self.left_road_markings, = ax.plot(x1, y, 'w--', linewidth=2, zorder=3)
        self.right_road_markings = ax.plot(x2, y, "w--", linewidth=2, zorder=3)

        return []


if __name__ == "__main__":
    import doctest
    doctest.testmod()

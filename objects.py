import matplotlib

class Lane():
    def __init__(self, position):
        self.position = position

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""
        self.stop_line, = ax.plot([], [], 'ko', markersize=10)
        x, y = self.position
        ax.axvline(x, linestyle=":")
        self.text = ax.text(x, y, "|", rotation=0,
                verticalalignment='center', horizontalalignment='center')

        return [self.stop_line, self.text]

    def update_animation(self):
        """Update matplotlib animation for axes ax"""
        x, y = self.position
        # Redraw the car stop
        self.stop_line.set_data([x], [y])
        # Return the patches for matplotlib to update
        return [self.stop_line, self.text]

class Car():
    def __init__(self, ID, direction, speed, length=10):

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
        self.go = False
        self.status = ""

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""
        self.car_line, = ax.plot([], [], 'gs', markersize=self.length)
        x, y = self.position
        self.text = ax.text(x, y+3, str(self.ID),
                verticalalignment='bottom', horizontalalignment='center')
        return [self.car_line, self.text]

    def update_animation(self):
        """Update matplotlib animation for axes ax"""
        # Redraw the car
        x, y = self.position
        self.car_line.set_data([x], [y])
        # Update text position
        self.text.set_x(x)
        self.text.set_y(y+3)
        # Return the patches for matplotlib to update
        return [self.car_line, self.text]

class Bridge():
    def __init__(self, rel_length, lanes, cars):
        self.rel_length = rel_length
        self.lanes = lanes
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

        # Initialise all car stops
        for lane in self.lanes:
            patches += lane.init_animation(ax)

        # List of patches for matplotlib to update
        return patches

    def update_animation(self):
        """Update matplotlib animation for axes ax"""

        # Redraw self before child objects
        patches = self._update_animation()

        # Redraw car stops
        for lane in self.lanes:
            patches += lane.update_animation()

        # Redraw cars
        for car in self.cars:
            patches += car.update_animation()

        # List of patches for matplotlib to update
        return patches

    def _init_animation(self, ax):
        """Initialise self for animation in axes ax"""
        size = self.rel_length
        delta = size // 2
        ax.set_xlim([self.start-delta, self.end+delta])
        ax.set_ylim([-size//5, size//5])
        self.route_line, = ax.plot([], [], 'w-', linewidth=3)
        return [self.route_line]

    def _update_animation(self):
        """Redraw self for animation in axes ax"""
        xdata = [self.start, self.end]
        ydata = [0, 0]
        self.route_line.set_data(xdata, ydata)
        return [self.route_line]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

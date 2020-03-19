#!/usr/bin/env python3

from objects import Car
from model import BridgeSystem
from animation import animate_model

cars = [
    Car(1, 1, 1), Car(2, 1, 1), Car(3, 1, 1), Car(4, 1, 1), Car(5, 1, 1), Car(6, 1, 1), 
    Car(1, -1, 1), Car(2, -1, 1), Car(3, -1, 1), Car(4, -1, 1), Car(5, -1, 1), Car(6, -1, 1)
]

model = BridgeSystem(10, cars)

animate_model(model)
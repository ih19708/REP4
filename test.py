#!/usr/bin/env python3

from objects import Car, Lane
from model import BridgeSystem
from animation import animate_model

lanes = [
    Lane((0, 0)),
    Lane((100, 0))
]

cars = [
    Car(1, 1, 1), Car(2, 1, 1), Car(3, 1, 1), Car(4, 1, 1), Car(5, 1, 1), Car(6, 1, 1), 
    Car(1, -1, 1), Car(2, -1, 1), Car(3, -1, 1), Car(4, -1, 1), Car(5, -1, 1), Car(6, -1, 1)
]

model = BridgeSystem(100, lanes, cars)

animate_model(model)
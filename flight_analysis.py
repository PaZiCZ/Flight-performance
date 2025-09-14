# flight performance analysis code
import numpy as np
from ISA import air_density
from specifications import nv, nh, hmax, vmax
from constants import g

class FlightPerformance:
    def __init__(self, aircraft_data):
        self.data = aircraft_data
        self.altitudes = np.linspace(0, hmax, nh)

        # Preallocate speeds as a 2D array [nh x nv]
        self.speeds = np.zeros((nh, nv))

        for i, altitude in enumerate(self.altitudes):
            vstall = np.sqrt(
                2 * aircraft_data["mtow"] * g
                / (air_density(altitude) * aircraft_data["sref"] * aircraft_data["clmax"])
            )
            self.speeds[i, :] = np.linspace(vstall, vmax / 3.6, nv)

        print(self.speeds)

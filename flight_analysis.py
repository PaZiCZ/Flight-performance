# flight performance analysis code
import numpy as np
from ISA import air_density
from specifications import nv, nh, hmax, vmax
from constants import g

class FlightPerformance:
    def __init__(self, adata):
        self.data = adata
        self.altitudes = np.linspace(0, hmax, nh)

        # Preallocate speeds as a 2D array [nh x nv]
        self.speeds = np.zeros((nh, nv))

        for i, altitude in enumerate(self.altitudes):
            vstall = np.sqrt(
                2 * adata.mtow * g
                / (air_density(altitude) * adata.sref * adata.clmax)
            )
            self.speeds[i, :] = np.linspace(vstall, vmax / 3.6, nv)

        print(self.speeds)

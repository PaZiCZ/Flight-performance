# flight performance analysis code
import numpy as np
from ISA import air_density
from specifications import nv, nh, hmax, vmax
from constants import g
from power import power_available

class FlightPerformance:
    def __init__(self, adata):
        self.data = adata
        self.altitudes = np.linspace(0, hmax, nh)
        # Preallocate speeds as a 2D array [nh x nv]
        self.speeds = np.zeros((nh, nv))
        self.cL = np.zeros((nh, nv))
        self.cD = np.zeros((nh, nv))
        self.D = np.zeros((nh, nv))
        self.Pa = np.zeros((nh, nv))
        self.Ta = np.zeros((nh, nv))
        self.Pr = np.zeros((nh, nv))
        self.intersections = []

    def compute_performance(self, adata):
        ar = adata.bref ** 2 / adata.sref

        for i, altitude in enumerate(self.altitudes):
            vstall = np.sqrt(
                2 * adata.mtow * g
                / (air_density(altitude) * adata.sref * adata.clmax)
            )
            self.speeds[i, :] = np.linspace(vstall, vmax / 3.6, nv)

        for i, altitude in enumerate(self.altitudes):
            rho = air_density(altitude)
            for j, speed in enumerate(self.speeds[i, :]):
                self.cL[i, j] = 2 * adata.mtow * g / (rho * adata.sref * speed ** 2)
                self.cD[i, j] = adata.cd0 + self.cL[i,j] ** 2 / (np.pi * ar * adata.e)
                self.D[i, j] = self.cD[i, j] * 0.5 * adata.sref * rho * speed ** 2
                self.Pa[i, j] = power_available(rho, speed, adata) * 1000
                self.Ta[i, j] = self.Pa[i, j] / speed
                self.Pr[i, j] = self.D[i, j] * speed

        print(self.Pa)
        print(self.Ta)


    def find_intersections(self):
        nh, nv = self.speeds.shape
        for i in range(nh):
            diff = self.Pa[i, :] - self.Pr[i, :]
            idx = np.where(np.diff(np.sign(diff)) != 0)[0]
            inter_speeds = []
            for j in idx:
                x0, x1 = self.speeds[i, j], self.speeds[i, j+1]
                y0, y1 = diff[j], diff[j+1]
                if y1 - y0 != 0:
                    x_int = x0 - y0 * (x1 - x0) / (y1 - y0)
                    inter_speeds.append(x_int)
            self.intersections.append(inter_speeds)
        return self.intersections


    def print_results(self):
        for i, inter in enumerate(self.intersections):
            print(f"Altitude {self.altitudes[i]:.0f} m: Intersection speeds = {inter}")


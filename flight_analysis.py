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
        self.w = np.zeros((nh, nv))

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
                self.w[i,j] = (self.Pa[i, j] - self.Pr[i, j]) / adata.mtow / g

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

    def find_ceiling(self):
        # Extract the two highest altitude indices
        h1 = self.altitudes[-2]
        h2 = self.altitudes[-1]

        # Find max climb rates at those altitudes
        w1 = np.max(self.w[-2, :])
        w2 = np.max(self.w[-1, :])

        # Linear extrapolation: w = a * h + b
        # Solve for a and b using the two points (h1, w1) and (h2, w2)
        a = (w2 - w1) / (h2 - h1)
        b = w1 - a * h1

        # Absolute ceiling: climb rate = 0
        if a != 0:
            h_abs = -b / a
        else:
            h_abs = np.nan  # No change in climb rate, ceiling undefined

        # Service ceiling: climb rate = 0.5 m/s
        h_serv = (0.5 - b) / a if a != 0 else np.nan

        return h_abs, h_serv

    def compute_turn_radius(self, adata):
        """
        Compute minimum turn radius at sea level for structural, aerodynamic, and power limitations.
        Returns a dictionary with speed array and corresponding radii for each limitation.
        """
        rho = air_density(0)
        ar = adata.bref ** 2 / adata.sref
        h_index = 0  # sea level
        speeds = self.speeds[h_index, :]
        D = self.D[h_index, :]
        Ta = self.Ta[h_index, :]
        cD0 = adata.cd0
        e = adata.e
        S = adata.sref
        m = adata.mtow
        n_max = adata.loadfactor

        # Stall speed at sea level
        vstall = np.sqrt(2 * m * g / (rho * S * adata.clmax))

        # Vmax from intersection speeds
        intersection_speeds = self.intersections[h_index]
        vmax = max(intersection_speeds) if intersection_speeds else speeds[-1]

        r_structural = []
        r_aero = []
        r_power = []

        for i, v in enumerate(speeds):
            # Structural limitation
            r_structural.append(v ** 2 / (g * np.sqrt(n_max ** 2 - 1)))

            # Aerodynamic limitation
            if v >= vstall:
                n_aero = (v / vstall) ** 2
                if n_aero > 1:
                    r_aero.append(v ** 2 / (g * np.sqrt(n_aero ** 2 - 1)))
                else:
                    r_aero.append(np.nan)
            else:
                r_aero.append(np.nan)

            # Power limitation
            if v <= vmax:
                cD = 2 * D[i] / (rho * S * v ** 2)
                if cD - cD0 > 0:
                    cL = np.sqrt((cD - cD0) * (np.pi * ar * e))
                    n_power = cL / cD * Ta[i] / m / g
                    if n_power > 1:
                        r_power.append(v ** 2 / (g * np.sqrt(n_power ** 2 - 1)))
                    else:
                        r_power.append(np.nan)
                else:
                    r_power.append(np.nan)
            else:
                r_power.append(np.nan)

        return {
            "speeds": speeds,
            "r_structural": np.array(r_structural),
            "r_aero": np.array(r_aero),
            "r_power": np.array(r_power)
        }


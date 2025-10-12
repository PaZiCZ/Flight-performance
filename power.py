# power_estimation.py
from constants import rho0


def calculate_propeller_efficiency(speed, vnom, etaprop):
    """
    Calculate propeller efficiency as a function of speed.

    Parameters:
    - speed (float): Aircraft speed in m/s
    - vnom (float): Nominal speed in m/s
    - etaprop (float): Maximum propeller efficiency

    Returns:
    - propeff (float): Propeller efficiency
    """
    L = speed / vnom * 3.6
    E = 1 - (1 - L) ** 2 * (1 + (0.8722 * L ** 2 - 1.3959 * L))
    return E * etaprop


def power_available(rho, speed, adata):
    """
    Calculate power available at a given air density (rho, kg/m3) and speed (m/s).
    Uses universal propeller efficiency characteristics and altitude characteristics.
    """
    if adata.engtype == 1:
        # altitude characteristics of reciprocating engine
        pmaxh = adata.pmax * (1.132 * rho / rho0 - 0.132)
    elif adata.engtype == 2:
        # altitude characteristics of turboprop engine
        pmaxh = adata.pmax * (rho / rho0) ** 0.7
    else:
        raise ValueError(f"Unknown engine type: {adata.engtype}")

    # propeller efficiency
    propeff = calculate_propeller_efficiency(speed, adata.vnom, adata.etaprop)

    # Total power in kW
    total_power = pmaxh * propeff

    return total_power

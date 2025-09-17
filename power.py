from constants import rho0

def power_available(rho, speed, adata):
    """
    Calculate power required at a given air density (rho, kg/m3) and speed (m/s).
    Uses universal propeller efficiency characteristics and altitude characteristics.
    """
    # altitude characteristics
    pmaxh = adata.pmax * (1.132 * rho / rho0 - 0.132)

    # propeller efficiency
    L = speed / adata.vnom * 3.6
    E = 1 - (1 - L) ** 2 * (1 + (0.8722 * L ** 2 - 1.3959 * L))
    propeff = E * adata.etaprop

    # Total power in kw
    total_power = pmaxh * propeff

    return total_power

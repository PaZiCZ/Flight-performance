from constants import rho0

def power_available(rho, speed, adata):
    """
    Calculate power available at a given air density (rho, kg/m3) and speed (m/s).
    Uses universal propeller efficiency characteristics and altitude characteristics.
    """
    if adata.engtype == 1:
        # altitude characteristics op reciprocating engine
        pmaxh = adata.pmax * (1.132 * rho / rho0 - 0.132)
    elif adata.engtype == 2:
        # altitude characteristics op turboprop engine
        pmaxh = adata.pmax * (rho / rho0) ** 0.7
    else:
        raise ValueError("Unknown engine type: {}".format(adata.engtype))

    # propeller efficiency
    L = speed / adata.vnom * 3.6
    E = 1 - (1 - L) ** 2 * (1 + (0.8722 * L ** 2 - 1.3959 * L))
    propeff = E * adata.etaprop

    # Total power in kw
    total_power = pmaxh * propeff

    return total_power

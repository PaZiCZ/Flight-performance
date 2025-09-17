# Function to calculate air density based on altitude using ISA model
# Assumes altitude < 11,000 m
from constants import rho0

def air_density(altitude_m):

    # Density from ideal gas law
    density = rho0 * (1 - altitude_m / 44308) ** 4.2553
    return density
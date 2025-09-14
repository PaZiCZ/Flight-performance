# Function to calculate air density based on altitude using ISA model
# Assumes altitude < 11,000 m

def air_density(altitude_m):
    # Constants
    sea_level_density = 1.225  # kg/m^3

    # Density from ideal gas law
    density = sea_level_density * (1 - altitude_m / 44308) ** 4.2553
    return density
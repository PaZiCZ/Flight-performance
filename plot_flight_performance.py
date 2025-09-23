
import matplotlib.pyplot as plt
import numpy as np

def plot_flight_performance(altitudes, stall_speeds, intersection_speeds):
    """
    Plot stall speed and maximum intersection speed vs altitude.
    Args:
        altitudes (array-like): Altitude values (y-axis)
        stall_speeds (array-like): Stall speed at each altitude (x-axis)
        intersection_speeds (list of lists): List of intersection speeds for each altitude
    """
    altitudes = np.array(altitudes)
    stall_speeds = np.array(stall_speeds)
    # Extract the maximum intersection speed for each altitude (if any)
    max_intersection_speeds = np.array([
        max(speeds) if speeds else np.nan for speeds in intersection_speeds
    ])

    plt.figure(figsize=(8, 6))
    plt.plot(stall_speeds, altitudes, label='Stall Speed', marker='o')
    plt.plot(max_intersection_speeds, altitudes, label='Max Intersection Speed', marker='x')
    plt.xlabel('Speed [m/s]')
    plt.ylabel('Altitude [m]')
    plt.title('Flight Envelope: Stall and Max Intersection Speeds vs Altitude')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

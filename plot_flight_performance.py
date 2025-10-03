
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def timestamp():
    """Generate a timestamp string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def plot_flight_envelope(altitudes, stall_speeds, intersection_speeds, save_dir="."):
    """
    Save stall speed and max intersection speed vs altitude to a PDF file.
    """
    altitudes = np.array(altitudes)
    stall_speeds = np.array(stall_speeds)
    max_intersection_speeds = np.array([
        max(speeds) if speeds else np.nan for speeds in intersection_speeds
    ])

    plt.figure(figsize=(8, 6))
    plt.plot(stall_speeds * 3.6, altitudes, label='Stall Speed', marker='o')  # km/h
    plt.plot(max_intersection_speeds * 3.6, altitudes, label='Max Intersection Speed', marker='x')
    plt.xlabel('Speed [km/h]')
    plt.ylabel('Altitude [m]')
    plt.title('Flight Envelope: Stall and Max Intersection Speeds vs Altitude')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename = f"flight_envelope_{timestamp()}.pdf"
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path)
    plt.close()
    print(f"Flight envelope plot saved as {os.path.abspath(save_path)}")


def plot_climb_rate(altitudes, speeds, climb_rates, save_dir="."):
    """
    Save climb rate vs speed for each altitude to a PDF file.
    """
    plt.figure(figsize=(8, 6))
    for i, altitude in enumerate(altitudes):
        speeds_kmh = speeds[i, :] * 3.6
        plt.plot(speeds_kmh, climb_rates[i, :], label=f"{int(altitude)} m")

    plt.xlabel("Speed [km/h]")
    plt.ylabel("Climb rate w [m/s]")
    plt.title("Climb Rate vs Speed at Different Altitudes")
    plt.legend(title="Altitude")
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.tight_layout()

    filename = f"climb_rate_{timestamp()}.pdf"
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path)
    plt.close()
    print(f"Climb rate plot saved as {os.path.abspath(save_path)}")

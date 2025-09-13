import matplotlib.pyplot as plt
import numpy as np
from readplane import aircraft_input as readinput

def print_parameters(data):
    print(f"Aircraft: {data.get('Plane', 'Unknown')}")
    print("Parameters:")
    for key, value in data.items():
        if key != 'Plane':
            print(f"  {key}: {value}")

# Function to modify parameters
def modify_parameters(data):
    print("Current parameters:")
    for key in data:
        if key != 'Plane':
            print(f"{key}: {data[key]}")
    param = input("Enter the parameter name to modify: ")
    if param in data:
        new_value = input(f"Enter new value for {param}: ")
        try:
            data[param] = float(new_value)
            print(f"Updated {param} to {data[param]}")
        except ValueError:
            print("Invalid value. Must be a number.")
    else:
        print("Parameter not found.")

# Dummy flight performance analysis function
def flight_performance_analysis(data):
    print("Running flight performance analysis...")
    if 'Power' in data and 'MTOW' in data:
        thrust_to_weight = data['Power'] / data['MTOW']
        print(f"Thrust-to-weight ratio: {thrust_to_weight:.3f}")
    else:
        print("Required parameters missing for analysis.")

# Main menu loop
def main():
    aircraft_data = {}
    while True:
        print("Main Menu")
        print("1) Read the input file")
        print("2) Plot the aircraft parameters")
        print("3) Modify aircraft parameters")
        print("4) Run flight performance analysis")
        print("5) Quit the program")
        choice = input("Enter your choice: ")

        if choice == '1':
            inputfile = input("Enter the input file name: ")
            aircraft_data = readinput(inputfile)
            print("Aircraft data loaded.")
        elif choice == '2':
            if aircraft_data:
                print_parameters(aircraft_data)
            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '3':
            if aircraft_data:
                modify_parameters(aircraft_data)
            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '4':
            if aircraft_data:
                flight_performance_analysis(aircraft_data)
            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option (number from 1 to 5).")

if __name__ == "__main__":
    main()
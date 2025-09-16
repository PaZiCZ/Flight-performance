import matplotlib.pyplot as plt
import numpy as np
from readplane import aircraft_input
from flight_analysis import FlightPerformance

def print_parameters(adata):
    plane = getattr(adata, "plane", "Unknown")
    print(f"Aircraft: {plane}\n")
    print("Parameters:")
    for section, keys in adata._sections.items():
        print(f"{section}:")
        for key in keys:
            value = getattr(adata, key, None)
            print(f"  {key}: {value}")
        print()

# Function to modify parameters
def modify_parameters(adata):
    print("Current parameters:")
    for section, keys in adata._sections.items():
        print(f"{section}:")
        for key in keys:
            print(f"  {key}: {getattr(adata, key)}")
        print()
    param = input("Enter the parameter name to modify: ")
    if hasattr(adata, param):
        new_value = input(f"Enter new value for {param}: ")
        try:
            setattr(adata, param, float(new_value))
            print(f"Updated {param} to {getattr(adata, param)}")
        except ValueError:
            print("Invalid value. Must be a number.")
    else:
        print("Parameter not found.")

# Main menu loop
def main():
    adata = None
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
            adata = aircraft_input(inputfile)
            print("Aircraft data loaded.")
        elif choice == '2':
            if adata:
                print_parameters(adata)
            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '3':
            if adata:
                modify_parameters(adata)
            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '4':
            if adata:
                FlightPerformance(adata)
            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option (number from 1 to 5).")

if __name__ == "__main__":
    main()
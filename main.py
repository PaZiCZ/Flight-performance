from readplane import aircraft_input
from flight_analysis import FlightPerformance
from plot_flight_performance import plot_flight_envelope
from plot_flight_performance import plot_climb_rate
from plot_flight_performance import plot_turn_diagram
from plot_flight_performance import plot_range
from plot_flight_performance import plot_endurance
import joke

def print_parameters(adata):
    plane = getattr(adata, "name", "Unknown")
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
        print("7) Print of joke of the day from https://jokesoftheday.net/")
        choice = input("Enter your choice: ")

        if choice == '1':
            inputfile = input("Enter the input file name: ")
            adata = aircraft_input(inputfile)
            if adata is None:
                print("Aircraft data loading FAILED.")
            else:
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
                fp = FlightPerformance(adata)
                fp.compute_performance(adata)  # Fills all the arrays with calculated data
                fp.find_intersections()  # Finds intersection points using the calculated data

                altitudes = fp.altitudes
                stall_speeds = fp.speeds[:, 0]  # First column is stall speed at each altitude
                intersections = fp.intersections
                ceiling = fp.find_ceiling()
                turn_data = fp.compute_turn_radius(adata)
                plot_flight_envelope(altitudes, stall_speeds, intersections, ceiling, aircraft_name=adata.name)
                plot_climb_rate(altitudes, fp.speeds, fp.w, aircraft_name=adata.name)
                plot_turn_diagram(turn_data, aircraft_name=adata.name)
                plot_range(altitudes, fp.speeds, intersections, fp.R, aircraft_name=adata.name)
                plot_endurance(altitudes, fp.speeds, intersections, fp.E, aircraft_name=adata.name)

            else:
                print("No data loaded. Please read the input file first.")
        elif choice == '7':
            print("\nJoke of the Day:\n")
            print(joke.get_joke_of_the_day())
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option (number from 1 to 5 or 7).")

if __name__ == "__main__":
    main()
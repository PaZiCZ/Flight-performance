class Adata:
    """Class for aircraft data with attribute-style access."""
    def __init__(self, data_dict, sections):
        for key, value in data_dict.items():
            setattr(self, key, value)
        self._sections = sections

def aircraft_input(filename):
    data = {}
    sections = {}
    current_section = None
    param_names = []
    errors = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        if line.startswith("Plane"):
            # Save aircraft name under 'name' key
            aircraft_name = line.split(" ", 1)[1]
            data['name'] = aircraft_name
        elif line.startswith("#"):
            param_names = line[1:].split()
        elif line.isupper():
            current_section = line
            sections[current_section] = []
        elif param_names:
            values = line.split()
            for name, value in zip(param_names, values):
                try:
                    data[name] = float(value)
                except ValueError:
                    errors.append(
                        f"!!! Line {line_num}, Section '{current_section}': "
                        f"Invalid non-numeric value '{value}' for parameter '{name}'"
                    )
                else:
                    if current_section:
                        sections[current_section].append(name)
            param_names = []

            if errors:
                print("\n!!!  The input data contains invalid values:\n")
                for err in errors:
                    print(err)
                print("\nReturning to main menu...\n")
                return None

    return Adata(data, sections)

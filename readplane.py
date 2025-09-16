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

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("Plane"):
            data['Plane'] = line.split(" ", 1)[1]
        elif line.startswith("#"):
            param_names = line[1:].split()
        elif line.isupper():
            current_section = line
            sections[current_section] = []
        elif param_names:
            values = line.split()
            for name, value in zip(param_names, values):
                # Try to cast to float if numeric /// zkontrolovat a doplnit kontrolu, ze promenne jsou numericke hodnoty
                try:
                    data[name] = float(value)
                except ValueError:
                    data[name] = value
                if current_section:
                    sections[current_section].append(name)
            param_names = []

    return Adata(data, sections)

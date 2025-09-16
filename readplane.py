def aircraft_input(filename):
    data = {}
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
            continue  # Skip group headers
        elif param_names:
            values = line.split()
            for name, value in zip(param_names, values):
                # Try to cast to float if numeric
                try:
                    data[name] = float(value)
                except ValueError:
                    data[name] = value
            param_names = []

    return data

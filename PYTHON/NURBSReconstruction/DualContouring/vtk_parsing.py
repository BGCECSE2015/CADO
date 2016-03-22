
__author__ = 'erik'

def parse_file_vtk(filename):
    import numpy as np
    with open(filename, 'r', ) as aFile:

        dimensions = []
        origin = []
        spacing = []

        for line in aFile:
            if 'DIMENSIONS' in line:
                linesplit = line.rsplit()
                dimensions = [int(linesplit[1]), int(linesplit[2]), int(linesplit[3])]
                break

        for line in aFile:
            if 'ORIGIN' in line:
                linesplit = line.rsplit()
                origin = [float(linesplit[1]), float(linesplit[2]), float(linesplit[3])]
                break

        for line in aFile:
            if 'SPACING' in line:
                linesplit = line.rsplit()
                spacing = [float(linesplit[1]), float(linesplit[2]), float(linesplit[3])]
                break

        for line in aFile:
            if 'POINT_DATA' in line:
                linesplit = line.rsplit()
                num_cells = int(linesplit[1])
                break

        for line in aFile:
            if 'LOOKUP_TABLE' in line:
                break

        array_index = 0
        values = np.zeros(num_cells, dtype=bool)

        print values
        for line in aFile:
            for word in line.rsplit():
                if array_index < num_cells:
                    values[array_index] = bool(int(word))
                    array_index += 1
                else:
                    return dimensions, origin, spacing, values
        return dimensions, origin, spacing, values
import csv
import scipy

def write_matrix_to_csv(matrix, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in matrix:
            csvwriter.writerow(row[:])

def write_matrix_to_asc(matrix, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in matrix:
            csvwriter.writerow(row[:])

def write_tensor3_to_csv(tensor, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in tensor:
            csvwriter.writerow(row.T.flatten())


def read_matrix_from_csv(filename):
    matrix = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            matrix.append(row)
    return scipy.array(matrix)

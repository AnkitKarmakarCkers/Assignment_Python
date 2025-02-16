import csv

def readFile(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)  # Read CSV into a list of lists
    
    width = get_width(data)  # Get column widths
    printTable(width, data)  # Print table

def get_width(data):
    # Find max width for each column
    return [max(len(str(item)) for item in col) for col in zip(*data)]

def printTable(width, data):
    # Create border
    border = '+'.join('-' * (w + 2) for w in width)
    border = f"+{border}+"
    
    print(border)  # Print top border
    
    for i, row in enumerate(data):
        row_str = '| ' + ' | '.join(f"{str(item).ljust(w)}" for item, w in zip(row, width)) + ' |'
        print(row_str)
        if i == 0:  # Print border after header
            print(border)
    
    print(border)  # Print bottom border

# Specify the CSV file path
csv_file = "/home/ankit/Assignment_Python/CSV_Example2.csv"
readFile(csv_file)

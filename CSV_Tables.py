import csv

def readFile(filename):
    with open(filename, newline='',encoding='utf-8') as file:
        reader=csv.reader(file)
        data=list(reader)
    return(get_width(data))

def get_width(data):
    width=[]
    for col in zip(*data):
        lengths=[len(str(item)) for item in col]
        width.append(max(lengths))
    return printTable(width,data)

def printTable(width,zipped_data):
    border='+'.join('-'*(w+2) for w in width)
    border=f"+{border}+"

    print(border)

    for i,row in enumerate(zipped_data):
        row_str='| ' + ' | '.join(f"{str(item).ljust(w)}" for item, w in zip(row, width))+' |'
        print(row_str)
        if i==0:
            print(border)
    print(border)

csv_file="/home/ankit/Assignment_Python/CSV_Example2.csv"
readFile(csv_file)

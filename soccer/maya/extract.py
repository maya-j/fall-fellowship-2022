"""Extracts MLS data into a dict"""

def get_data():
    import csv

    data = {}
 
    # opening and reading the CSV file
    with open('mls_2016.csv', mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            if line[0] != "Club":
                data[line[0]] = {"goals_scored": int(line[6]), 
                "goals_allowed": int(line[7]), "actual_win_percentage": float(line[3])/float(line[1])}

    return data

if __name__=="__main__":
    get_data()
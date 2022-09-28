import csv
import json


csvFile='C:\Download\CSV\file1.csv';
jsonFile='C:\Download\CSV\file2.json';

data={}
with open(csvFile) as csvFile:
    csvReader=csv.DictReader(csvFile)
    for rows in csvReader:
        id=rows['ID']
        data[id]=rows

with open(jsonFile,'w') as jsonFile:
    jsonFile.write(json.dumps(data,indent=4))


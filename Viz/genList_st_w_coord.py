import json
import os
import csv

printed_messages = set()
dir = "../DataScrape/JourneyDetail_data"
files = os.listdir(dir)

trains_dict = {}
dataset_dict = {}

def load_data(file):
    with open(f"../DataScrape/JourneyDetail_data/{file}",'r') as input:
        data = json.load(input)
        input.close()
        return data

def get_line_info(data):
    trainName = data["Product"][0]["name"]
    trains_dict[trainName] = {'stops':[],'coordinates':[]}
    for station in data["Stops"]["Stop"]:
        trains_dict[trainName]['stops'].append(station["name"])
        lon = station["lon"]
        lat = station["lat"]
        trains_dict[trainName]['coordinates'].append((lon,lat))

def create_dataset():
    for train in trains_dict:
        for i,stop in enumerate(trains_dict[train]['stops']):
            cleaned_stop = stop.replace(" st.", "").replace(" St.", "").strip()
            if cleaned_stop not in dataset_dict:
                dataset_dict[cleaned_stop] = trains_dict[train]["coordinates"][i]


def write_dataset():
    with open("coordinates.csv", 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['station','lon','lat'])
        for station in dataset_dict:
            row = [station]
            row.append(dataset_dict[station][0])
            row.append(dataset_dict[station][1])
            writer.writerow(row)
    outfile.close()

def main():
    for file in files:
        get_line_info(load_data(file))
    create_dataset()

    write_dataset()

if __name__ == '__main__':
    main()
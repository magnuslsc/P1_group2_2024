import os 
import json 
import math
import pandas as pd


printed_messages = set()
dir = "JourneyDetail_data"
files = os.listdir(dir)

trains_dict = {}
dataset_dict = {}
# Prints trainName, first and last stops of all found trains.
def printstationslist(data):
        end = len(data["Stops"]["Stop"])-1
        first_stop = data["Stops"]["Stop"][0]["name"]
        last_stop = data["Stops"]["Stop"][end]["name"]
        trainName = data["Product"][0]["name"]
        message = f"{first_stop} -> {last_stop}"
        
        if message not in printed_messages:
            print(f"train: {trainName}",message)
            printed_messages.add(message)

def import_paastiger_csv(filename='paastiger_data.csv'):
    try:
        csv = pd.read_csv(filename, sep=';')
        return csv
    except FileNotFoundError:
        print("Error: paastiger_data.csv file not found")
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty")
    except Exception as e:
        print(f"Error loading CSV: {e}")

#loads a given json file. 
def load_journeydetail_data(file):
    with open(f"JourneyDetail_data/{file}",'r') as input:
        data = json.load(input)
        input.close()
        return data
    
def get_line_info(data):
    if data["Product"][0]["operator"] != "Skånetrafiken":
        trainName = data["Product"][0]["name"]
        trains_dict[trainName] = {'stops':[],'coordinates':[]}
        for station in data["Stops"]["Stop"]:
            cleaned_name = station["name"].replace(" st.", "").replace(" St.", "").strip()
            trains_dict[trainName]['stops'].append(cleaned_name)
            lon = station["lon"]
            lat = station["lat"]
            trains_dict[trainName]['coordinates'].append((lon,lat))

def pandafilter(csv):
    csv['Total'] = pd.to_numeric(csv['Total'].str.replace('.', ''), errors='coerce').astype('Int64')
    f_csv = csv[csv['Stationsnavn'] != 'lokaltog']
    ff_csv = f_csv[f_csv['Total'] != '0']
    fff_csv = ff_csv.loc[:, ['Stationsnavn', 'Total']]
    return fff_csv

def createNewDataset(f_csv,dataset):
    for i,station in enumerate(dataset): 
        if station[0] in f_csv['Stationsnavn'].values:
            total = f_csv.loc[f_csv['Stationsnavn'] == station[0], 'Total'].values[0]
            dataset[i].insert(1,total)
    return dataset

def writeNewDataset(dataset):
        with open("newDataset.txt",'w') as outfile: 
            for line in dataset:
                for elm in line: 
                    outfile.write(str(elm))
                    outfile.write(',')
                outfile.write('\n')
        outfile.close()
        return "SUCCES"


def create_dataset(paastiger):
    """
    Creates the dataset from trains_dict

    dataset structure is defined as: 
        {stationName:{connectsTo[],DistBetween[]}}
    """
    for train in trains_dict:
        l = len(trains_dict[train]["stops"]) 
        for i in range(l-1):
            currSt = trains_dict[train]["stops"][i+1]
            currCoord = trains_dict[train]["coordinates"][i+1]

            prevSt = trains_dict[train]["stops"][i]
            prevCoord = trains_dict[train]["coordinates"][i]

            dist = calc_dist(currCoord,prevCoord)

            if prevSt in dataset_dict:
                if currSt in dataset_dict[prevSt]["connectsTo"]:
                    continue
                else:    
                    dataset_dict[prevSt]["connectsTo"].append(currSt)
                    dataset_dict[prevSt]["dist"].append(dist)
            else:    
                dataset_dict[prevSt] = {'connectsTo':[],'dist':[]}
                dataset_dict[prevSt]["connectsTo"].append(currSt)
                dataset_dict[prevSt]["dist"].append(dist)


    
# Add one connection to from source to input, with distance
# Next feature is to add which trainline is connecting them. 
def write_dataset(paastiger):
    with open("../program/dataset.txt",'w') as outfile:
        for station in dataset_dict:
            paastiger_value = paastiger.loc[paastiger['Stationsnavn'] == station, 'Total'].values[0]
            length = len(dataset_dict[station]["connectsTo"])
            outfile.write(station)
            outfile.write(",")
            outfile.write(f"{paastiger_value},")
            for i in range(length):
                outfile.write(dataset_dict[station]["connectsTo"][i])
                outfile.write(",")
                outfile.write(str(dataset_dict[station]["dist"][i]))
                outfile.write(",")
            outfile.write("\n")
            missing = ['Varde','Struer','Nykøbing F','Hjørring']
        for station in missing:
            outfile.write(station)
            outfile.write(',')
            outfile.write('0')
            outfile.write('\n')
    outfile.close()


# calculates distance between 2 sets of coordinates. 
def calc_dist(c1,c2):
        # Convert latitude and longitude from degrees to radians
    phi1 = math.radians(c1[1])
    phi2 = math.radians(c2[1])
    delta_phi = math.radians(c2[1] - c1[1])
    delta_lambda = math.radians(c2[0] - c1[0])

    # Haversine formula
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Earth's radius in kilometers (use 3956 for miles)
    radius = 6371.0

    # Calculate the distance
    distance = (radius * c)
    #distance = ((radius * c)/ paastiger_avg) * 10**6
    return "{:.3f}".format(distance)

def main():
    dir = "JourneyDetail_data"
    files = os.listdir(dir)

    for file in files:
    #file = "IC 152.json"
        print(f"________ loading {file} __________" )
        get_line_info(load_journeydetail_data(file))
        print("succesful load of data")

    for train in trains_dict:
        print(f"________ {train} __________" )

        length = len(trains_dict[train]['stops'])
        for i in range(length):
            print("station: ", trains_dict[train]["stops"][i],"Coordinates: ", trains_dict[train]["coordinates"][i])
    
    print("________ Creating dataset________")
    paastiger = pandafilter(import_paastiger_csv())
    create_dataset(paastiger)
    print("Created dataset")

    print("________ Writing dataset________")
    write_dataset(paastiger)
    print("dataset.txt succesfully written")

if __name__ == '__main__':
    main()
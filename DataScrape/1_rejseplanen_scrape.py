import json
import requests
import os 
import sys

def init_folders():
    paths = ["DepatureBoard_data/raw","DepatureBoard_data/formated","JourneyDetail_data"]
    for path in paths:
        if os.path.exists(path):
            print(f"{path} already exisists")
        else:
            os.makedirs(path,exist_ok=True)

base_url = "https://www.rejseplanen.dk/api/"
def scrape_locationdetail(station):
    endpoint = "location.name"

    params = {
        "accessId": f"{key}",
        "format": "json",
        "input":f"{station}"
    }
    url = f"{base_url}{endpoint}"

    response = requests.get(url, params=params)
    if response.status_code ==200: 
        try: 
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError:
            print("Response content is not valid JSON")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)        

#Done
def find_stationId(station,StationId_dict):
    data = scrape_locationdetail(station)
    item = data["stopLocationOrCoordLocation"][0]
    StationId_dict[station] = item["StopLocation"]["id"]
    print(f"StationId succesfully loaded for {station}")

#DONE
def scrape_depatureBoard(stationId_dict):
    for station in stationId_dict:    
        endpoint = "departureBoard"
        params = {
            "accessId": f"{key}",
            "format": "json",
            "id":f"{stationId_dict[station]}"
        }
        # Construct the full URL
        url = f"{base_url}{endpoint}"
        # Make the GET request
        response = requests.get(url, params=params)
        # Check the response status
        if response.status_code == 200:
            try:
                # Parse the JSON response
                data = response.json()  # Use response.text if the response is XML
                # Write the data to a file
                with open(f'DepatureBoard_data/raw/response_depatureboard_{station}.json', 'w') as file:
                    json.dump(data, file, indent=4)
                print(f"Data written to response_depatureboard_{station}.json")
            except requests.exceptions.JSONDecodeError:
                print("Response content is not valid JSON")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

# Removes every depature that is not, trains.
def format_depatureBoard(stationId_dict):
    '''
    Removes every depature that is not trains. 
    This is defined by the field found in (departure["Product"][0]["icon"]["res"]) where it needs to "prod_ic"
    '''
    for station in stationId_dict:
        with open(f'DepatureBoard_data/raw/response_depatureboard_{station}.json',"r") as input_file:
            input = json.load(input_file)
        input_file.close()
        with open(f'DepatureBoard_data/formated/formated_depatureboard_{station}.json', "a") as out:
            out.write("{\"Depature\":[")
            for departure in input["Departure"]:
                if departure["Product"][0]["icon"]["res"] == "prod_ic":
                    json.dump(departure, out,indent=4)
                    out.write(',\n')
            out.write("{}]}")
        out.close()
        print(f"Depature board of {station} formatted")

def scrape_journeyDetail(refId,trainName):
    endpoint = "journeyDetail"
    params = {
        "accessId": f"{key}",
        "format": "json",
        "id":f"{refId}"
    }
    # Construct the full URL
    url = f"{base_url}{endpoint}"
    # Make the GET request
    response = requests.get(url, params=params)
    # Check the response status
    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = response.json()  # Use response.text if the response is XML
            # Write the data to a file
            file_path = f'JourneyDetail_data/{trainName}.json'

            if os.path.exists(file_path):
                print(f"{trainName} Already scraped")
            else:
                with open(f"JourneyDetail_data/{trainName}.json",'w') as out:
                    json.dump(data,out,indent=4)
                    print(f"{trainName} Scraped succesfully")
        except requests.exceptions.JSONDecodeError:
            print("Response content is not valid JSON")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# def format_JourneyD(data):
#     return None

# Get all stations from a journey Ref. 
def get_JourneyDetail():
    dir = 'DepatureBoard_data/formated'
    entries = os.listdir(dir)

    for filename in entries:
        with open(f"{dir}/{filename}",'r') as input:
            inputData = json.load(input)
            for elm in inputData["Depature"]: 
                if len(elm) != 0:
                    ref = elm["JourneyDetailRef"]["ref"]
                    trainName = elm["Product"][0]["name"]
                    scrape_journeyDetail(ref,trainName)
                else:    
                    break
                    


def main():
    init_folders()
    #init api-key 
    try:
        with open("key.txt", 'r') as akey:
            global key
            key = akey.readline().rstrip('\n')
    except FileNotFoundError:
        print("Error: key.txt file not found, pls create it and try again.")
        sys.exit(1)  # Terminate the program with a non-zero exit code

    # Init list of stations to scrape
    station_arr = ["København","Aarhus","Roskilde","Fredericia","Aalborg","esbjerg","vejle"]
    stationId_dict = {}

    print("___________Scraping Depature Boards:___________")
    #find stationID for all stations
    for stations in station_arr:
        find_stationId(stations,stationId_dict)


    #scrape depatureboard
    scrape_depatureBoard(stationId_dict)
    
    #Export all train journey from depatureBoards.
    print("___________Starting Formatting:___________")
    format_depatureBoard(stationId_dict)

    print("___________Getting journeyDetails:___________")
    #Scrape station from all train journeys

    get_JourneyDetail()
    print("___________Done with journeyDetails:___________")
    

if __name__ == '__main__':
    main()
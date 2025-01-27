import pandas as pd 
import matplotlib.pyplot as plt
import math


def edges():
    edges_arr = []
    with open(f"../program/output.txt",'r') as edges:
        for line in edges:
            edges_arr.append(line.strip().split(','))
    edges.close()
    return edges_arr

def find_coord_from_edges(edges_arr,station_coords):
    '''Outputs a list of tuples(lon,lat) containing list coord. '''
    out = []
    for line in edges_arr:
        source = line[0]
        dest = line[1]
        w = line[-1]
        data = station_coords.query(f'station == "{source}" or station =="{dest}"')
        lon = data['lon'].tolist()
        lat = data['lat'].tolist()
        out.append((lon,lat,w))
    return out


def plot_lines(lines):
    fig, ax = plt.subplots()

    for triples in lines:
        x = [float(triples[0][0]), float(triples[0][1])]
        y = [float(triples[1][0]), float(triples[1][1])]
        
        # Convert string to float and normalize to 0-1 range for colormap
        try:
            weight = float(triples[2])/10**6
            # Assuming weights are between 0-100, normalize to 0-1
            sigmoid_weight = 1 / (1 + math.exp(-weight))
            normalized_weight = (sigmoid_weight-0.5)/0.5
            color = plt.cm.coolwarm(normalized_weight)
        except ValueError:
            # Use default color if weight cannot be converted to float
            color = 'red'
            
        ax.plot(x, y, marker='o', color=color)

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)
    plt.show()

def plotmap(easting,northing):
    plt.plot(edges[0],edges[1],marker ='o')
    plt.figure(figsize=(8,6))  # optional: sets the figure size
    plt.scatter(easting, northing, marker='o', color='blue', edgecolor='black')
    plt.title('Plot of Coordinates Without a Map')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)  # optional: add a grid for reference
    plt.show()



def main():
    station_coords = pd.read_csv('Coordinates.csv')

    egde_arr = edges()
    lines = find_coord_from_edges(egde_arr,station_coords)

    plot_lines(lines)

if __name__ == "__main__":
    main()
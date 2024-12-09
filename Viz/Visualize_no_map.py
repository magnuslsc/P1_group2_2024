# import osmnx as ox
# import networkx as nx
# import matplotlib.pyplot as plt

# # Define the place of interest
# place_name = "Copenhagen, Denmark"

# # Retrieve the railway network
# G = ox.graph_from_place(place_name, network_type='all', custom_filter='["railway"~"station|rail"]')

# # Plot the graph
# fig, ax = ox.plot_graph(G, node_size=10, node_color='red', edge_color='black', edge_linewidth=1.0)

import pandas as pd 
import matplotlib.pyplot as plt
from pyproj import Transformer

def init_transformer(station_coords):
    crs_wgs84 = "EPSG:4326"      # WGS84 Latitude/Longitude
    crs_utm33n = "EPSG:32633"    # UTM Zone 33N
    
    transformer = Transformer.from_crs(crs_wgs84,crs_utm33n,always_xy=True)
    
    longitudes = station_coords['lon'].to_list()
    latitudes = station_coords['lat'].tolist()

    return transformer.transform(longitudes,latitudes)

def edges():
    edges_arr = []
    with open("edges.txt",'r') as edges:
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

def float_to_rgb_colormap(value, colormap_name='viridis'):
    rgb = plt.cm.viridis(value)  # This returns values in 0-1 range
    return rgb


def plot_lines(lines):
    fig, ax = plt.subplots()
    
    for triples in lines:
        x = [float(triples[0][0]), float(triples[0][1])]
        y = [float(triples[1][0]), float(triples[1][1])]
        
        # Convert string to float and normalize to 0-1 range for colormap
        try:
            weight = float(triples[2])
            # Assuming weights are between 0-100, normalize to 0-1
            normalized_weight = weight / 100.0
            color = plt.cm.viridis(normalized_weight)
        except ValueError:
            # Use default color if weight cannot be converted to float
            color = 'blue'
            
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

    easting,northing = init_transformer(station_coords)

    egde_arr = edges()
    lines = find_coord_from_edges(egde_arr,station_coords)

    #plotmap(lines,easting,northing)
    plot_lines(lines)

if __name__ == "__main__":
    main()
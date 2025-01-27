# P1_Project - How does DSB implement eletrical trains efficiently?
## Participants
- Magnus Levanius Schouw Christiansen
- Andreas Foverskov
- Luke Veilleux
- Magnus Kronby Jakobsen
- Navinder Singh
- Nikolaj Lütken
- Rohan Atik 

## Important Dependencies
- Python 3.12
- requests
    ``pip install requests``
- Pandas
    ``pip install pandas``
- matplotlib
    ``pip install matplotlib``
- geopandas (maybe)
    ``pip install geopandas``


## How to use the project 
Step 0: Run the scraping
    This step requires the user to have an API-key to rejseplanen.dk. 
    We have for safety reasons not included the API-key in the repository.
    The API-key should be placed in the file `key.txt` in the 'Data' folder

    To run the scraping, run the following command from the DataScrape folder
    ``python3 -m 1_rejseplanen_scrape``

### Running the project automatically
To run every step of the project run the following commands from the P1_GROUP2_2024
    ``chmod +x run_project.sh``
    ``./run_project.sh``
*IMPORTANT* wont run without the above mentioned Dependencies.

### Running the project manually
Step 1: Creating the dataset
    to create the dataset, run the following command from the DataScrape folder
    ``python3 -m 2_toDataset``

Step 2: Running model
    to run the modelling, run the following command' from the 'program' folder
    ``gcc gcc main.c shortest_path.c min_heap/min_heap.c data_to_graph.c``
    ``./a.out dataset.txt 146``

Step 3: Run the Visualisation
    to run the visualisation, run the following command from the 'Viz' folder
    ``python3 -m Visualisation_no_map``

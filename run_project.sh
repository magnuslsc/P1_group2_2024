#!/bin/bash

# Step 1: Run the Python script to create the dataset
echo "------------------------"
echo "Running 2_toDataset.py..."
cd DataScrape
python3 2_toDataset.py
cd .. 

# Step 2: Compile all C files in the program folder
echo "------------------------"
echo "Compiling C files in the program folder..."
cd program
gcc main.c shortest_path.c min_heap/min_heap.c data_to_graph.c


# Step 3: Run the compiled C program with the specified arguments
echo "Running the compiled C program..."
./a.out dataset.txt 146
cd ..

# Step 4: Run the Python script for visualization
echo "------------------------"
echo "Running Visualize_no_map.py..."
cd Viz
python3 Visualize_no_map.py
cd .. 

echo "All tasks completed."
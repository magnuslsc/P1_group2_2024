#pragma once

#include "data_to_graph.h"

int bfs(Station** stations, int visited[], int source, int target, int* path, int num_nodes);
int dfs(Station** stations, int source, int target, int* visited, int* path, int index);
void print_path(Station** stations, int* path, int len);
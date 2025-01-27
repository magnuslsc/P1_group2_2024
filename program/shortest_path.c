#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>

#include "data_to_graph.h"
#include "shortest_path.h"


int path_find_init(Graph* network, int source, int target, int num_nodes) {
    MinHeap* heap = initialize_heap(source, num_nodes);

    int** paths_id = malloc(num_nodes * sizeof(int *));
    for (int i = 0; i < num_nodes; i++) {
        paths_id[i] = malloc(num_nodes * sizeof(int));
    }

    for (int i = 0; i < num_nodes; i++) {
        for (int j = 0; j < num_nodes; j++) {
            paths_id[i][j] = -1;
        }
    }

    double* path_sums = malloc(num_nodes * sizeof(double));
    for (int i = 0; i < num_nodes; i++) {
        if (i != source) {
            path_sums[i] = (double)INT_MAX;
        } else {
            path_sums[i] = 0.0;
        }
    }

    double path_to_target = compute_path(network->stations, heap, path_sums, source, target, paths_id);

    for (int i = 0; i < num_nodes; i++){
    	int j = 0;
    	double accum = 0;
    	while (paths_id[i][j] != -1){
    		ListNode* curr = find_edge(network, paths_id[i][j]);
    		int pass = curr->passengers_avg;
			if(accum == 0){
				accum = (pow(2, -(curr->distance / 79.4))) * (double)pass;
			}
			else{
				accum = accum * (pow(2, -(curr->distance / 79.4))) + (double)pass;
			}
    		curr->ret_val += accum;
    		j++;
    	}
    }

    for (int i = 0; i < num_nodes; i++){
        free(paths_id[i]);
    }
    free(paths_id);
    free(path_sums);

    return path_to_target;
}

int compute_path(Station** stations, MinHeap* heap, double* path_sums, int source, int target, int** paths_id){
	while (heap->size != 0){
		HeapNode curr_node = extract_min(heap);

		if (path_sums[curr_node.node] == (double)INT_MAX){
			break;
		}

		ListNode* neighbor = stations[curr_node.node]->list_head->next;

		while (neighbor){
			double new_dist = neighbor->weight + path_sums[curr_node.node];
			if (path_sums[neighbor->idx_in_arr] > new_dist){
				path_sums[neighbor->idx_in_arr] = new_dist;
				decrease_node_val(heap, neighbor->idx_in_arr, path_sums[neighbor->idx_in_arr], heap->positions);
				update_paths_id(stations, paths_id, curr_node.node, neighbor);
			}
			neighbor = neighbor->next;
		}
	}
	return path_sums[target];
}

// void update_paths_id(Station** stations, int** paths_id, int from, int to){
// 	ListNode* curr = stations[from]->list_head->next;
// 	while (curr->idx_in_arr != to){
// 		curr = curr->next;
// 	}
// 	int i = 0;
// 	while (paths_id[to][i + 1] != -1){
// 		i++;
// 	}
// 	paths_id[to][i] = curr->edge_id;
// }

void update_paths_id(Station** stations, int** paths_id, int from, ListNode* neighbor){
	int i = 0; 
	while(paths_id[neighbor->idx_in_arr][i+1]!=-1){
		i++;
	}
	paths_id[neighbor->idx_in_arr][i] = neighbor->edge_id;
}





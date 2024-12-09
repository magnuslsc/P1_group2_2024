#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include "data_to_graph.h"
#include "shortest_path.h"

int path_find_init(Station** stations, int source, int target, int num_nodes){
	MinHeap* heap = initialize_heap(source, num_nodes);
	int path_sums[num_nodes];
	for (int i = 0; i < num_nodes; i++){
		if (i != source){
			path_sums[i] = INT_MAX;
		}
		else {
			path_sums[i] = 0;
		}
	}
	int path_to_target = compute_path(stations, heap, path_sums, source, target);

	printf("Source is %s\n\n", stations[source]->name);

	for (int i = 0; i < num_nodes; i++){
		printf("Path-cost from source to %s is %d\n", stations[i]->name, path_sums[i]);
	}

	return path_to_target;
}

int compute_path(Station** stations, MinHeap* heap, int* path_sums, int source, int target){
	while (heap->size != 0){
		HeapNode curr_node = extract_min(heap);

		if (path_sums[curr_node.node] == INT_MAX){
			break;
		}

		ListNode* neighbor = stations[curr_node.node]->list_head->next;

		while (neighbor){
			int new_dist = neighbor->weight + path_sums[curr_node.node];
			if (path_sums[neighbor->idx_in_arr] > new_dist){
				path_sums[neighbor->idx_in_arr] = new_dist;
				
				decrease_node_val(heap, neighbor->idx_in_arr, path_sums[neighbor->idx_in_arr], heap->positions);

				neighbor->times_visited++;
			}
			neighbor = neighbor->next;
		}
	}
	return path_sums[target];
}







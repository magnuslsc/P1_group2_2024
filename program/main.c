#include "data_to_graph.h"
#include "shortest_path.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void output_file(Graph* network);
double calc_passengers(Graph* network, char* a, char* b);

int main(int argc, char** argv){
	Graph* network = create_graph(argv[1], atoi(argv[2]));

	for (int i = 0; i < network->num_stations; i++){
		int path_cost = path_find_init(network, i, (i + 1) % network->num_stations, network->num_stations);
		if (path_cost == 2147483647){
			path_cost = -1;
		}
		continue;
	}
	output_file(network);
	for (int i = 0; i < network->num_stations; i++){
		free_adj_list(network->stations[i]->list_head);
		free(network->stations[i]);
	}
	free(network->stations);
	free(network);
}

void output_file(Graph* network){
	FILE* out = fopen("output.txt", "w");
	for (int i = 0; i < network->num_stations; i++){
		Station* station = network->stations[i];
		ListNode* curr = network->stations[i]->list_head->next;
		while (curr != NULL){
            fprintf(out, "%s,%s,%.3lf\n", network->stations[curr->idx_in_arr]->name, network->stations[i]->name, curr->ret_val);
			curr = curr->next;
        }
	}
	fclose(out);
}

double calc_passengers(Graph* network, char* a, char* b){
	int pass_a = 0;
	int pass_b = 0;

	for (int i = 0; i < network->num_stations; i++){
		if (strcmp(network->stations[i]->name, a)){
			pass_a = network->stations[i]->passengers;
		}
		else if (strcmp(network->stations[i]->name, b)){
			pass_b = network->stations[i]->passengers;
		}
	}
	return (double)(pass_a + pass_b) / 2.0;
}



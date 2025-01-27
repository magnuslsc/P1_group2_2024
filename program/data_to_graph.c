#include "data_to_graph.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


Graph* create_graph(char* filename, int num_stations){
    int current_edge_id = 0;
    Graph* network = (Graph*)malloc(sizeof(Graph));
    network->num_stations = num_stations;

    network->stations = (Station**)malloc(sizeof(Station*) * network->num_stations);

    FILE* pF = fopen(filename, "r");

    if (pF == NULL) {
        exit(EXIT_FAILURE);
    }

    char buffer[256];
    int index = 0;

    while (fgets(buffer, sizeof(buffer), pF)) {
        int len = strlen(buffer);

        if (buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }

        if (index >= num_stations) {
            printf("Number of stations in file does not match expected amount. Program will now exit.\n");
            for (int i = 0; i < index; i++){
                free(network->stations[i]);
            }
            free(network->stations);
            free(network);
            exit(EXIT_FAILURE);
        }
        char* station_name = strtok(buffer, ",");
        int pass = atoi(strtok(NULL, ","));
        network->stations[index] = create_station(station_name, pass);
        index++;
    }

    if (index < num_stations - 1) {
            printf("Number of stations in file does not match expected amount. Program will now exit.\n");
            for (int i = 0; i < index; i++){
                free(network->stations[i]);
            }
            free(network->stations);
            free(network);
            exit(EXIT_FAILURE);
        }

    rewind(pF);

    index = 0;
    while (fgets(buffer, sizeof(buffer), pF)){
        int len = strlen(buffer);
        if (buffer[len - 1] == '\n'){
            buffer[len - 1] = '\0';
        }
        int numeric = 0;
        int curr_idx = -1;
        char* curr;

        curr = strtok(buffer, ",");
        create_linked_list_head(network->stations[index], index);
        strtok(NULL, ",");
        ListNode* last_node = network->stations[index]->list_head;

        while ((curr = strtok(NULL, ",")) != NULL) {
            if (numeric == 0) {
                curr_idx = get_idx(network->stations, network->num_stations, curr);
                if (curr_idx == -1) {
                    printf("Station '%s' not found.\n", curr);
                    printf("During %s linked list, index: %d.\n", network->stations[index]->name, index);
                    break;
                }
                numeric = 1;
            } 
            else {
                ListNode* new_node = (ListNode*)malloc(sizeof(ListNode));
                new_node->idx_in_arr = curr_idx;
                new_node->weight = calc_weight(network, network->stations[index], network->stations[curr_idx], atof(curr));
                new_node->distance = atof(curr);
                new_node->edge_id = current_edge_id++;
                new_node->passengers_avg = ((network->stations[index]->passengers + network->stations[curr_idx]->passengers) / 2);
                new_node->ret_val = 0.0;
                new_node->next = NULL;
                last_node->next = new_node;
                last_node = new_node;

                numeric = 0;
            }
        }
        index++;
    }
    fclose(pF);

    return network;
}

Station* create_station(char name[], int val){
    Station* new_station = (Station*)malloc(sizeof(Station));
    strcpy(new_station->name, name);
    new_station->list_head = NULL;
    new_station->passengers = val;

    return new_station;
}

void create_linked_list_head(Station *station_head, int index){
    ListNode* head = (ListNode*)malloc(sizeof(ListNode));
    head->next = NULL;
    head->weight = 0;
    head->idx_in_arr = index;
    station_head->list_head = head;
}

void free_adj_list(ListNode* head){
    ListNode* temp;
    while (head != NULL){
        temp = head;
        head = head->next;
        free(temp);
    }
}

int get_idx(Station** stations, int len, char* name){
    for (int i = 0; i < len; i++) {
        if (strcmp(stations[i]->name, name) == 0){
            return i;
        }
    }
    return -1;
}

ListNode* find_edge(Graph* network, int edge_id) {
    for (int i = 0; i < network->num_stations; i++) {
        ListNode* current = network->stations[i]->list_head;
        while (current != NULL) {
            if (current->edge_id == edge_id) {
                return current;
            }
            current = current->next;
        }
    }
    return NULL;
}


double calc_weight(Graph* network, Station* st_a, Station* st_b, double distance){
    return 1 / ((((double)st_a->passengers + (double)st_b->passengers) / 2) / distance);
}









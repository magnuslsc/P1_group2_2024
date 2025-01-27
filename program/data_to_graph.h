#pragma once

typedef struct ListNode {
    int idx_in_arr;
    int weight;
    int edge_id;
    double passengers_avg;
    double ret_val;
    double distance;
    struct ListNode* next;
} ListNode;

typedef struct Station {
    char name[50];
    ListNode* list_head;
    int passengers;
} Station;

typedef struct Graph {
    int num_stations;
    Station** stations;
} Graph;

Graph* create_graph(char* filename, int num_stations);
Station* create_station(char name[], int val);
void create_linked_list_head(Station* station_head, int index);
void free_adj_list(ListNode* head);
int get_idx(Station** stations, int len, char* name);
ListNode* find_edge(Graph* network, int edge_id);
int get_edge_times_visited(int edge_id);
double calc_weight(Graph* network, Station* st_a, Station* st_b, double distance);
#include "min_heap/min_heap.h"

int path_find_init(Graph* network, int source, int target, int num_nodes);
int compute_path(Station** stations, MinHeap* heap, double* path_sums, int source, int target, int** paths_id);
void update_paths_id(Station** stations, int** paths_id, int from, ListNode* neighbor);
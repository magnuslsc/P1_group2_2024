#define MAX_SIZE 158
#define NUM_STATIONS 158

typedef struct HeapNode {
    int node;
    double distance;
} HeapNode;

typedef struct MinHeap {
    HeapNode data[MAX_SIZE];
    int positions[MAX_SIZE];
    int size;
} MinHeap;

void swap(MinHeap *heap, int index1, int index2, int *positions);
MinHeap* initialize_heap(int source, int num_nodes);
void heapify_down(MinHeap* heap, int index);
HeapNode extract_min(MinHeap *heap);
void heapify_up(MinHeap* heap, int index, int* positions);
void insert_element(MinHeap* heap, HeapNode value, int* positions);
void decrease_node_val(MinHeap* heap, int node_index, double new_distance, int* positions);
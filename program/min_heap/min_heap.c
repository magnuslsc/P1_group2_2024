#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include "min_heap.h"

void swap(MinHeap* heap, int index1, int index2, int* positions){
    HeapNode temp = heap->data[index1];
    heap->data[index1] = heap->data[index2];
    heap->data[index2] = temp;

    heap->positions[heap->data[index1].node] = index1;
    heap->positions[heap->data[index2].node] = index2;
}

MinHeap* initialize_heap(int source, int num_nodes){
    MinHeap* new_heap = (MinHeap*)malloc(sizeof(MinHeap));
    new_heap->size = 0;

    for (int i = 0; i < num_nodes; i++){
        if (i == source){
            insert_element(new_heap, (HeapNode){i, 0}, new_heap->positions);
        }
        else {
            insert_element(new_heap, (HeapNode){i, INT_MAX}, new_heap->positions);
        }
    }
    return new_heap;
}

void heapify_down(MinHeap* heap, int index){
    int smallest = index;
    int left = 2 * index + 1;
    int right = 2 * index + 2;

    if (left < heap->size && heap->data[left].distance < heap->data[smallest].distance){
        smallest = left;
    }

    if (right < heap->size && heap->data[right].distance < heap->data[smallest].distance){
        smallest = right;
    }

    if (smallest != index) {
        swap(heap, smallest, index, heap->positions);
        heapify_down(heap, smallest);
    }
}

HeapNode extract_min(MinHeap* heap){
    if (heap->size <= 0){
        printf("Heap is empty\n");
        return (HeapNode){-1, -1};
    }

    HeapNode root = heap->data[0];
    heap->data[0] = heap->data[--heap->size];

    heapify_down(heap, 0);

    return root;
}

void heapify_up(MinHeap* heap, int index, int* positions){
    while (index != 0 && heap->data[(index - 1) / 2].distance > heap->data[index].distance){
        positions[heap->data[index].node] = (index - 1) / 2;
        positions[heap->data[(index - 1) / 2].node] = index;

        swap(heap, index, (index - 1) / 2, heap->positions);
        index = (index - 1) / 2;
    }
}

void insert_element(MinHeap* heap, HeapNode value, int* positions){
    if (heap->size == MAX_SIZE) {
        printf("Heap is full\n");
        return;
    }

    int i = heap->size++;
    heap->data[i] = value;
    positions[value.node] = i;

    heapify_up(heap, i, positions);
}

void decrease_node_val(MinHeap* heap, int node_index, double new_distance, int* positions){
    int i = heap->positions[node_index];
    heap->data[i].distance = new_distance;

    heapify_up(heap, i, positions);
}


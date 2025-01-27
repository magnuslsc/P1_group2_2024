#include "traverse.h"

#include <stdio.h>

int bfs(Station** stations, int visited[], int source, int target, int* path, int num_nodes){
    int queue[num_nodes];
    int front = 0, rear = 0;

    visited[source] = 1;

    queue[rear++] = source;

    int previous[num_nodes];
    for (int i = 0; i < num_nodes; i++){
        previous[i] = -1;
    }

    while(front < rear){
        int current = queue[front++];
        if (current == target){
            break;
        }

        ListNode* current_adj = stations[current]->list_head->next;
        
        while(current_adj != NULL){
            int neighbor = current_adj->idx_in_arr;

            if (!visited[neighbor]){
                visited[neighbor] = 1;
                queue[rear++] = neighbor;
                previous[neighbor] = current; 
            }

            current_adj = current_adj->next;
        }
    }

    int path_len = 0;
    int path_index = target;
    while(path_index != -1){
        path[path_len++] = path_index;
        path_index = previous[path_index];
    }

    return path_len;
}

int dfs(Station** stations, int source, int target, int* visited, int* path, int index){
    visited[source] = 1;
    path[index] = source;
    
    if (source == target) {
        return index;
    }
    
    ListNode* temp = stations[source]->list_head->next;
    int path_found;
    while (temp != NULL){
        if (!visited[temp->idx_in_arr]){
            if ((path_found = dfs(stations, temp->idx_in_arr, target, visited, path, index + 1))){
                return path_found;
            }
        }
        temp = temp->next;
    }
    path[index] = -1;
    return 0;
}
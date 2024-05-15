import os
from a1Queue import Queue

def inputFile(filename):
    arr = []
    with open(filename, "r") as file:
        for line in file:
            row = []
            for char in line.strip():
                row.append(char)
            arr.append(row)
        
    return arr

def printArray(arr):
    for row in arr:
        print(' '.join(row))


def returnStart(arr):
    x = None # return row
    y = None # return col
    for row_id, row in enumerate(arr):
        for col_id, col in enumerate(row):
            if col == 'S':
                x = row_id
                y = col_id
                return x, y
    return x, y

def length(arr):
    rows = len(arr)
    cols = len(arr[0])
    return rows, cols

def bfs(arr, start_x, start_y, length_rows, length_cols):
    q = Queue()
    q.enqueue((start_x, start_y, 0))
    visited = set()
    visited.add((start_x, start_y))
    parent = {}
    while not q.is_empty():
        #input("Press Enter to continue to the next iteration...")
        #os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        #print("Iteration:", count)
        #count += 1
        #printArray(arr)  # Print the maze
        current_x, current_y, path_length = q.dequeue()
        if arr[current_x][current_y] == 'E':
            path_x = current_x
            path_y = current_y
            start_x, start_y = returnStart(arr)
            while (path_x != start_x) or (path_y != start_y):
                #print("We're in this while loop")
                arr[path_x][path_y] = '*'
                path_x, path_y = parent[(path_x, path_y)]
            arr[current_x][current_y] = 'E'
            return current_x, current_y, arr, path_length
        else:
            for dx, dy, direction in [(1, 0, '.'), (-1, 0, '.'), (0, 1, '.'), (0, -1, '.')]:
                new_x, new_y = current_x + dx, current_y + dy
                if (new_x >= 0 and new_x < length_rows) and (new_y >= 0 and new_y < length_cols) and (arr[new_x][new_y] != 'X') and ((new_x, new_y) not in visited):
                    if (arr[new_x][new_y] != 'E'):
                        arr[new_x][new_y] = direction
                    q.enqueue((new_x, new_y, path_length + 1))
                    visited.add((new_x, new_y))
                    parent[(new_x, new_y)] = (current_x, current_y)
    return None, None, arr, path_length


# Testing input code 
#filename = "pathFindingMap.txt"
#arr = inputFile(filename)
#printArray(arr)

if __name__ == "__main__":
    #filename = input("Enter name of file: ")
    filename = "pathFindingMap.txt"
    arr = inputFile(filename)
    printArray(arr)
    length_rows, length_cols = length(arr)
    start_x, start_y = returnStart(arr)
    print("S is at", start_x, ",", start_y)
    x, y, arr, path_length = bfs(arr, start_x, start_y, length_rows, length_cols)
    print("End coordinates are:", x, ",", y)
    printArray(arr)
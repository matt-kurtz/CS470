import math
"""
class PriorityQueue:
    def __init__(self, start_x, start_y):
        self.items = []
        self.start = (start_x, start_y)

    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, coords):
        distance = math.sqrt((coords[0] - self.start[0])**2 + (coords[1] - self.start[1])**2)
        self.items.append((distance, coords))
        self.items.sort()
    

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop(0)

    def printQueue(self):
        for item in self.items:
            print(item)

"""
class PriorityQueue:
    def __init__(self, start_x, start_y, end_x=None, end_y=None):
        self.items = []
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        self.counter = 0  # Counter to maintain order of insertion

    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, coords):
        #distance = math.sqrt((coords[0] - self.start[0])**2 + (coords[1] - self.start[1])**2)
        pl = coords[2]
        self.items.append((pl, self.counter, coords))
        self.counter += 1  # Increment counter
        self.sort()

    # enqueuing using a*. Essentially the enqueue function above, but we add the distance to the path length as an heuristic
    def enqueue_a(self, coords):
        distance = math.sqrt((coords[0] - self.end[0])**2 + (coords[1] - self.end[1])**2)
        pl = coords[2]
        self.items.append((pl + distance, self.counter, coords))
        self.counter += 1
        self.sort()

    def enqueue_b(self, coords):
        distance = abs(coords[0] - self.end[0]) + abs(coords[1] - self.end[1])
        pl = coords[2]
        self.items.append((pl + distance, self.counter, coords))
        self.counter += 1
        self.sort()

    def sort(self):
        self.items.sort()  # Sort based on distance and insertion order
    
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop(0)[2]  # Return only the coordinates

    def printQueue(self):
        for item in self.items:
            print(item)


class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, coords):
        self.items.append(coords)
    
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop(0) #
        
    def size(self):
        return len(self.items)
    
    def is_empty(self):
        return len(self.items) == 0 #if len is 0, it's empty
    
    # Simply prints the queue
    def printQueue(self):
        for item in self.items:
            print(item)

# Making sure the queue works            
"""    
q = Queue()

for i in range(10):
    q.enqueue((i, i+1))

q.printQueue()

for i in range(5):
    q.dequeue()

q.printQueue()
"""
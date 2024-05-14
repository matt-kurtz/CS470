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
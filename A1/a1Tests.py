from a1Queue import PriorityQueue

start_x = 15
start_y = 15
q = PriorityQueue(start_x, start_y)
q.enqueue((15, 16))
q.enqueue((30, 40))
q.enqueue((2, 3))
q.printQueue()

d, coords = q.dequeue()
print(f"d: {d}, x: {coords[0]}, y: {coords[1]}")

#print(popped)
q.printQueue()
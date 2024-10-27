class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        
    def enqueue(self, data):
        new_node = Node(data)
        
        if not self.front:
            self.front = new_node
            self.rear = new_node
            return
        
        self.rear.next = new_node
        self.rear = new_node
        
    def dequeue(self):
        if not self.front:
            raise IndexError("dequeue from empty queue")
        
        removed = self.front
        self.front = self.front.next
        
        if not self.front:
            self.rear = None
        
        return removed.data
    
    def empty(self):
        return not self.front
    
    def peek(self):
        return self.front.data
    
    def size(self):
        size = 0
        current = self.front
        while current:
            current = current.next
            size += 1
        return size
    
    def __repr__(self): #controlamos lo que sale en consola cuando hacemos print
        output = ""
        current = self.front
        while current:
            output += f"{current.data} ->"
            current = current.next
        return output
    
    
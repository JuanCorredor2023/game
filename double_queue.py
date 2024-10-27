class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        
class Dequeue:
    def __init__(self):
        self.front = None
        self.rear = None
        
    def insert_front(self, data):
        new_node = Node(data)
        
        if not self.front:
            self.front = new_node
            self.rear = new_node
            return
        
        if self.front == self.rear:
            self.front = new_node
            self.front.next = self.rear
            self.rear.prev = self.front
            return
        
        new_node.next = self.front
        self.front.prev = new_node
        self.front = new_node
    
    def insert_rear(self, data):
        new_node = Node(data)
        
        if not self.front:
            self.front = new_node
            self.rear = new_node
            return
        
        if self.front == self.rear:
            self.rear = new_node
            self.front.next = self.rear
            self.rear.prev = self.front
            
        self.rear.next = new_node
        new_node.prev = self.rear
        self.rear = new_node
    
    def remove_front(self):
        if not self.front:
            return Exception("Cannot remove from empty queue")
        
        removed = self.front
        
        if self.front == self.rear:
            self.front = None
            self.rear = None
        else:
            self.front = self.front.next
            self.front.prev = None
            
        return removed
            
    
    def remove_rear(self):
        if not self.front :
            return Exception("Cannot remove from empty queue")
        
        removed = self.rear
        
        if self.front == self.rear:
            self.front = None
            self.rear = None
        else: 
            self.rear = self.rear.prev
            self.rear.next = None
        
        return removed
    
    def get_front(self):
        return self.front
    
    def get_rear(self):
        return self.rear
    
    def is_empty(self):
        return not self.front
    
    def size(self):
        if not self.front:
            return 0
        
        size = 1
        current = self.front
        while current != self.rear:
            current = current.next
            size += 1 
            
    def __repr__(self):
        if self.is_empty():
            return "Empty queue"
        if self.size() == 1:
            return f'{self.front}, '
        
        output = ""
        current = self.front
        while current != self.rear:
            output += f'{self.front}, '
            current = current.next
        return output
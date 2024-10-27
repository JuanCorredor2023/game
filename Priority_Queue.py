class PQueueSimple:
    def __init__(self):
        self.queue = []
        
    def enqueue(self, data):
        self.queue.append(data)
        self.queue.sort(reverse=True)
        
    def dequeue(self):
        if not self.queue:
            raise IndexError("dequeue from empty queue")
        
        return self.queue.pop(0)
    
    
    def peek(self):
        if not self.queue:
            raise IndexError("dequeue from empty queue")
        
        return self.queue[0]

    def size(self):
        return len(self.queue)
    
    def empty(self):
        return not self.queue

    def __repr__(self):
        return f'{self.queue}'

class PQueueAP:
    def __init__(self):
        self.queue = []
        
    def enqueue(self, priority, data):
        self.queue.append((priority, data))
        self.queue.sort(key=lambda x: x[0])
    
    def dequeue(self):
        if not self.queue:
            raise IndexError("dequeue from empty queue")
        
        priority, data = self.queue.pop(0)
        
        return priority, data
    
    def peek(self):
        if not self.queue:
            raise IndexError("peek from empty queue")
        
        return self.queue[0][0], self.queue[0][1]

    def size(self):
        return len(self.queue)
    
    def empty(self):
        return not self.queue

    def __repr__(self):
        return f'{self.queue}'
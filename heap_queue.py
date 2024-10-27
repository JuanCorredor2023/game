class Node:
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
        
class Heap:
    def __init__(self):
        self.__root = None
        self.__size = 0
        
    def enqueue(self, priority, data):
        new_node = Node(priority, data)
        
        if not self.__root:
            self.__root = new_node
        else:
            self.__insert_node(new_node)
            self.__bubble_up(new_node)
            
        self.__size += 1
    
    def __insert_node(self, new_node):
        path = bin(self.__size+1)[3:]
        current = self.__root
        parent = None
        
        for direction in path:
            parent = current
            current = current.left if direction == '0' else current.right
            
        new_node.parent = parent
        if not parent.left:
            parent.left = new_node
        else:
            parent.right = new_node 
            
    def dequeue(self):
        if not self.__root:
            raise IndexError("deque from empty queue")
            
        max_node = self.__root
        priority, data = max_node.priority, max_node.data
        
        if self.__size == 1:
            self.__root = None
        else:   
            last_node = self.__find_last_node()
            self.__swap(max_node, last_node)
            self.__remove_last_node()
            self.__bubble_down(self.__root)
            
        self.__size-=1
        
        return priority, data
            
    def __bubble_up(self, node):
        while node.parent:
            if node.parent.priority < node.priority:
                self.__swap(node.parent, node)
                node = node.parent
            else:
                break
            
    def __bubble_down(self, node):
        while node.left:
            bigger_child = node.left
            
            if node.right and node.right.priority > bigger_child.priority:
                bigger_child = node.right
                
            if node.priority < bigger_child.priority:
                self.__swap(node, bigger_child)
                node = bigger_child
            else:
                break
                
    def __swap(self, node1, node2):
        node1.priority, node2.priority = node2.priority, node1.priority
        node1.data, node2.data = node2.data, node1.data
        
    def __find_last_node(self):
        path = bin(self.__size)[3:]
        current = self.__root
        
        for direction in path:
            current = current.left if direction == '0' else current.right
        return current
    
    def __remove_last_node(self):
        path = bin(self.__size)[3:]
        current = self.__root
        parent = None
        
        for direction in path:
            parent = current
            current = current.left if direction =='0' else current.right
            
        if parent.left == current:
            parent.left = None
        else:
            parent.right = None
            
    def get_root(self):
        return self.__root
    
    def get_size(self):
        return self.__size
    
    def print_heap(self, node, n):
        if node:
            self.print_heap(node.left, n+1)
            print("       "*n + f"({node.priority}, {node.data}")
            self.print_heap(node.right, n+1)
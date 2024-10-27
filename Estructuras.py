from myqueue import Queue
from heap_queue import Heap
from double_queue import Dequeue
from Characters import  Villager, Lumberjack, Miner, Soldier

from abc import ABC, abstractmethod
import random

class ActionsQueue:
    def __init__(self):
        self.buffer = Queue()
        self.heap = Heap()
        
    def insert(self, action):
        self.buffer.enqueue(action)
        print("se inserto accion al buffer")
    
    def execute(self, poblacion):
        while self.buffer.size() > 0:
            i = self.buffer.dequeue()
            used = poblacion.usar(i)
            print (f"se emparejo la accion {i} con el personaje {used.number}")
            self.heap.enqueue(i, used)
        
        #self.heap.print_heap(self.heap.get_root(), 0)
        
        while self.heap.get_size() > 0:
            accion, personaje = self.heap.dequeue()
            if (accion == 0):
                personaje.cultivar()
                print(f"Se realizo la accion {accion}")
            elif (accion == 1):
                personaje.talar()
                print(f"Se realizo la accion {accion}")
            elif (accion == 2):
                personaje.minar()
                print(f"Se realizo la accion {accion}")
            elif (accion == 3):
                personaje.explorar()
                print(f"Se realizo la accion {accion}")
            elif (accion == 4):
                personaje.defensa()
                print(f"Se realizo la accion {accion}")
            poblacion.add(personaje.number)

class CharactersQueue:
    def __init__(self):
        self.characters = Dequeue()
        
    def add(self, character):
        if character == 0:
            personaje = Villager()
            self.characters.insert_front(personaje)
            print(f'se agrego un personaje tipo {character}')
        elif character == 1:
            personaje = Lumberjack()
            self.characters.insert_front(personaje)
            print(f'se agrego un personaje tipo {character}')
        elif character == 2:
            personaje = Miner()
            self.characters.insert_front(personaje)
            print(f'se agrego un personaje tipo {character}')
        elif character == 3:
            personaje = Soldier()
            self.characters.insert_front(personaje)
            print(f'se agrego un personaje tipo {character}')
        
    def usar(self, accion):
        current = self.characters.get_front()
        
        max_compatibility = current.data.actions[accion]
        max_comp_node = current
        while current:
            if current.data.number == accion:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                used = current
                break
            else:
                if current.data.actions[accion] > max_compatibility:
                    max_compatibility = current.data.actions[accion]
                    max_comp_node = current
                current = current.next 
        if not current:
            used = max_comp_node
            if used.prev:
                used.prev.next = used.next
            if used.next:
                used.next.prev = used.prev
            
        return used.data
        
class BuildingsQueue:
    def __init__(self):
        self.buildings = Dequeue()
    
    def build(self, building_type):
        self.buildings.insert_front(building_type)
    
    def wreck(self):
        self.buildings.remove_rear()
        
    def generate(self, poblacion):
        current = self.buildings.get_front()
        
        while current:
            for i in range (5):
                poblacion.add(current.data)
                
if __name__ == "__main__":
    import random
    Actions = ActionsQueue()
    Poblacion = CharactersQueue()
    Building = BuildingsQueue()
    
    for i in range(11):
        Poblacion.add(random.randint(0, 3))
        
    acciones = [2, 0, 1, 3, 4, 1, 0, 1, 2, 0, 3]
    
    for i in acciones:
        Actions.insert(i)
        
    Actions.execute(Poblacion)
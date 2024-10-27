from abc import ABC, abstractmethod
import random
import string

# Creacion de una clase base character
class Character(ABC):
    def __init__(self):
        self.actions = []
        #actions = [cultivar, talar, minar, explorar, defensa]
        self.invoke()
    
    @abstractmethod
    def invoke(self):
        pass
    
    def cultivar(self):
        r = random.randint(1, self.actions[0])
        with open("resources_vitacora.txt", 'a') as file:
            file.write(f"+{r} harvest")
        return r
    
    def talar(self):
        r = random.randint(1, self.actions[1])
        with open("resources_vitacora.txt", 'a') as file:
            file.write(f"+{r} wood")
        return r
    
    def minar(self):
        r = random.randint(1, self.actions[2])
        with open("resources_vitacora.txt", 'a') as file:
            file.write(f"+{r} mineral")
        return r
    
    def explorar(self):
        r = random.randint(1, self.actions[3])
        with open("resources_vitacora.txt", 'a') as file:
            file.write(f"+{r} point of knowledge")
        return r
    
    def defensa(self):
        r = random.randint(1, self.actions[4])
        
        return r
        
class Villager(Character):
    def __init__(self):
        super().__init__()
        self.number = 0
        self.actions = [4, 3, 2, 1, 1]
    
    def invoke(self):
        with open("generation_vitacora.txt", 'a') as file:
            file.write("+1 Villager\n")

class Lumberjack(Character):
    def __init__(self):
        super().__init__()
        self.number = 1
        self.actions = [2, 4, 1, 3, 2]
    
    def invoke(self):
        with open("generation_vitacora.txt", 'a') as file:
            file.write("+1 Lumberjack\n")
            
            
class Miner(Character):
    def __init__(self):
        super().__init__()
        self.number = 2
        self.actions = [1, 2, 4, 3, 2]
    
    def invoke(self):
        with open("generation_vitacora.txt", 'a') as file:
            file.write("+1 Miner\n")
        
class Soldier(Character):
    def __init__(self):
        super().__init__()
        self.number = 3
        self.actions = [2, 3, 1, 4, 4,]
    
    def invoke(self):
        with open("generation_vitacora.txt", 'a') as file:
            file.write("+1 Soldier\n")
            
    
    
    
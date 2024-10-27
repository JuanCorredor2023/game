from Estructuras import ActionsQueue, CharactersQueue, BuildingsQueue
import random

class Village:
    def __init__(self, year = 0, keepPlaying = True):
        self.year = year
        self.characters = CharactersQueue()
        self.buildings = BuildingsQueue()
        self.actions = ActionsQueue()
        self.characters.add(0)
        self.keepPlaying = keepPlaying
    
    def menuTasks(self):
        key = True
        while key == True:
            print("---------Tasks--------")
            print("1. Harvest")
            print("2. Collect Wood")
            print("3. Mine")
            print("4. Explore")
            print("5. Exit")
            print("Select an option")
            
            try:
                option = int(input("-> ->"))
            except ValueError:
                print("Warning: input must be a positive integer")
                continue
            
            if option == 1:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Tasks ->-> Harvest")
                self.actions.insert(0)
                # meter harvest en el buffer
            elif option == 2:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Tasks ->-> Collect Wood")
                self.actions.insert(1)
                # meter collect wood en el buffer
            elif option == 3:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Tasks ->-> Mine")
                self.actions.insert(2)
                # meter mine en el buffer
                pass
            elif option == 4:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Tasks ->-> Explore")
                #meter explore en el buffer
                self.actions.insert(3)
                pass
            elif option == 5:
                key = False # para regresar al menu
            else:
                print("Error occurred")
                continue
        self.menu()
            
                
    def menuBuildings(self):
        key = True
        while key == True:
            print("------Buildings-----")
            print("1. Villager's house")
            print("2. Workshop")
            print("3. Mine Shaft")
            print("4. Barraks")
            print("Select an option")
            try:
                option = int(input("-> ->"))
            except ValueError:
                print("Warning: input must be a positive integer")
                continue
            
            if option == 1:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Build ->-> Villager's House")
                self.buildings.build()
            elif option == 2:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Build ->-> Workshop")
                self.buildings.build()
                # meter collect wood en el buffer
            elif option == 3:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Build ->-> Mine Shaft")
                self.buildings.build()
                # meter mine en el buffer
            elif option == 4:
                with open("actions_vitacora.txt", 'a') as file:
                    file.write("-> Build ->-> Barracks")
                self.buildings.build()
                #meter explore en el buffer
            elif option == 5:
                key = False
                 # para regresar al menu
            else:
                print("Error occurred")
                continue
        self.menu()
        
    def menu(self):
        key = True
        while key == True:
            print(f"-----Year: {self.year}-----")
            print("1. Tasks")
            print("2. Buildings")
            print("3. Incursion")
            print("4. Excute")
            print("5. End Game")
            print("Select an option:")
            
            try:
                option = int(input("->"))
            except ValueError:
                print("Warning: input must be a positive integer")
                continue
            
            if option == 1:
                self.menuTasks()
                break
            elif option == 2:
                self.menuBuildings()
                break
            elif option == 3:
                self.incursion()
                break
                # empezar una incursion
            elif option == 4:
                self.year += 1
                with open("actions_vitacora.txt", 'a') as file:
                    file.write(f"------------------------{self.year}------------------------")
                self.actions.execute(self.characters)
                # para regresar al menu
                self.menu()
                break
                # Ejecutar
            elif option == 5:
                # me parece que lo mejor seria poner esto como joptionpane
                print("Are you sure you want to stop playing?")
                print("Keep in mind that you will loose your progress!")
                print("1. Yes")
                print("2. No")
                endingOption = input("Select an option:")
                
                try:
                    option = int(input("->"))
                except ValueError:
                    print("Warning: input must be a positive integer")
                    continue
                
                if endingOption == 1:
                    print("Closing the simulation...")
                    self.keepPlaying = False
                    # actualiza la llave keepPlaying para detener la simulacion
                else:
                    continue
                
            else:
                print("Error occurred")
                continue
    
    def incursion(self):
        print("An incursion is coming...")
        with open("actions_vitacora.txt", 'a') as file:
            file.write("-> Tasks ->-> Defend")
        pToken = int(self.characters.characters.size() / self.year)
        severityChar = random.randint(5, pToken)
        severityBuild =  int(severityChar/3)
        
        self.actions.insert(4)
        
        for i in range(severityChar):
            self.actions.insert(4)
            self.characters.characters.remove_front()
        
        for i in range(severityBuild):
            self.buildings.buildings.remove_front()
        
    
        
if __name__ == "__main__":
    v = Village()
    keepPlaying = True
    while v.keepPlaying:
        v.menu()
        
        
    
    
# Importación de módulos necesarios
import os                                  # Para operaciones del sistema operativo
import pygame                              # Biblioteca principal para crear el juego
import sys                                # Para funciones del sistema y salir del programa
from movement import MovementFunctions     # Importa funciones personalizadas de movimiento
import random                             # Para generar números aleatorios
import time                               # Para manejo de tiempo y delays
from Village import Village               # Importa la clase Village personalizada

# Configuración específica para macOS - establece el driver de video
os.environ['SDL_VIDEODRIVER'] = 'cocoa'
#os.environ['SDL_VIDEODRIVER'] = 'windows'  # Comentado - versión para Windows
############## change it if running in windows###################################

# Inicia todos los módulos de pygame
pygame.init()

# Crea una nueva instancia de la clase Village
village = Village()

# Define el tamaño de la ventana del juego
screen_width, screen_height = 1440, 810    # Ancho y alto en píxeles
screen = pygame.display.set_mode((screen_width, screen_height))  # Crea la ventana

# Define colores RGB básicos para usar en el juego
BLACK = (0, 0, 0)                         # Negro
WHITE = (255, 255, 255)                   # Blanco
GRAY = (128, 128, 128)                    # Gris
RED = (255, 0, 0)                         # Rojo
GREEN = (0, 255, 0)                       # Verde

# Inicializa el sistema de fuentes
pygame.font.init()
font = pygame.font.Font(None, 24)          # Crea una fuente de tamaño 24

# Carga y escala la imagen de fondo
background_image = pygame.image.load("fondo.png")  # Carga la imagen
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Ajusta al tamaño de pantalla

# Carga y escala la imagen del leñador
lumberjack_image = pygame.image.load("lenador.png")
lumberjack_image = pygame.transform.smoothscale(lumberjack_image, (80, 80))

# Carga y escala la imagen del minero
minero_image = pygame.image.load("minero.png")
minero_image = pygame.transform.smoothscale(minero_image, (80, 80))

# Carga y escala la imagen del aldeano
aldeano_image = pygame.image.load("aldeano.png")
aldeano_image = pygame.transform.smoothscale(aldeano_image, (80, 80))

# Carga y escala la imagen del soldado
soldado_image = pygame.image.load("soldado.png")
soldado_image = pygame.transform.smoothscale(soldado_image, (80, 80))

# Configuración de la consola lateral
console_width = 250                        # Ancho de la consola
console_height = screen_height             # Alto igual a la pantalla
console_surface = pygame.Surface((console_width, console_height))  # Superficie para la consola
console_text = []                          # Lista para almacenar el texto mostrado
input_text = ""                           # Variable para el texto de entrada
input_active = False                      # Estado de la entrada de texto

# Define los botones y sus posiciones
button_start_y = console_height - 350      # Posición Y inicial de los botones
buttons = [
    {"text": "1. Harvest", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y, 230, 35)},
    {"text": "2. Collect Wood", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y + 40, 230, 35)},
    {"text": "3. Mine", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y + 80, 230, 35)},
    {"text": "4. Explore", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y + 120, 230, 35)},
    {"text": "5. Exit", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y + 160, 230, 35)},
    {"text": "6. Attack!", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y + 200, 230, 35)},
    {"text": "7. Execute", "rect": pygame.Rect(screen_width - console_width + 10, button_start_y + 240, 230, 35)}
]

# Función para agregar texto a la consola
def add_to_console(text):
    console_text.append(text)              # Agrega el texto a la lista
    if len(console_text) > 15:            # Si hay más de 15 líneas
        console_text.pop(0)               # Elimina la línea más antigua

# Función para crear personajes con atributos iniciales
def create_characters(image, n, screen_width, screen_height):
    characters = []
    for _ in range(n):                    # Crea n personajes
        # Genera posición inicial aleatoria
        x = random.randint(0, screen_width - console_width)
        y = random.randint(0, screen_height)
        # Genera posición objetivo aleatoria
        target_x = random.randint(0, screen_width - console_width)
        target_y = random.randint(0, screen_height)
        # Crea diccionario con todos los atributos del personaje
        characters.append({
            "image": image,               # Imagen del personaje
            "x": x,                       # Posición X actual
            "y": y,                       # Posición Y actual
            "target_x": target_x,         # Objetivo X
            "target_y": target_y,         # Objetivo Y
            "scale": 100,                 # Escala de la imagen
            "mining": False,              # Estado de minería
            "mine_timer": 0,              # Temporizador de minería
            "collecting_wood": False,      # Estado de recolección
            "wood_timer": 0,              # Temporizador de recolección
            "wood_direction": 1,          # Dirección de movimiento
            "shake_offset": 0,            # Desplazamiento de temblor
            "reached_wood_point": False,   # Si llegó al punto de madera
            "exploring": False,           # Estado de exploración
            "explore_phase": 0,           # Fase de exploración
            "under_attack": False,        # Estado de ataque
            "harvesting": False,          # Estado de cosecha
            "harvest_timer": 0,           # Temporizador de cosecha
            "harvest_color": None         # Color durante cosecha
        })
    return characters

# Define cantidad de cada tipo de personaje
num_lumberjacks = 1                       # Número de leñadores
num_mineros = 1                           # Número de mineros
num_aldeanos = 1                         # Número de aldeanos
num_soldados = 1                         # Número de soldados

# Crea las listas de personajes usando la función create_characters
lumberjacks = create_characters(lumberjack_image, num_lumberjacks, screen_width, screen_height)
mineros = create_characters(minero_image, num_mineros, screen_width, screen_height)
aldeanos = create_characters(aldeano_image, num_aldeanos, screen_width, screen_height)
soldados = create_characters(soldado_image, num_soldados, screen_width, screen_height)

# Define velocidad de movimiento
speed = 1                                 # Velocidad base de movimiento

# Variables de estado del juego
under_attack = False                      # Estado de ataque inicial
attack_start_time = 0                     # Tiempo de inicio del ataque

# Objeto para controlar FPS
clock = pygame.time.Clock()

# Inicializa el texto de la consola
add_to_console("---------Tasks--------")
add_to_console("Select an option (1-6)")
add_to_console("1. Harvest")
add_to_console("2. Collect Wood")
add_to_console("3. Mine")
add_to_console("4. Explore")
add_to_console("5. Exit")
add_to_console("6. Attack!")

# Bucle principal del juego
running = True                            # Control del bucle principal
while running:
    # Procesa todos los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      # Si se cierra la ventana
            pygame.quit()                  # Cierra pygame
            sys.exit()                    # Termina el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic
            mouse_pos = pygame.mouse.get_pos()      # Obtiene posición del mouse
            # Verifica si se hizo clic en algún botón
            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):  # Si el clic fue en un botón
                    if button["text"] == "1. Harvest":      # Botón de cosecha
                        # Inicia acción de cosecha
                        village.actions.insert(0)
                        add_to_console("Harvesting...")
                        center_x = (screen_width - console_width) // 2
                        center_y = screen_height // 2
                        for aldeano in aldeanos:            # Configura cada aldeano
                            aldeano["target_x"] = center_x + random.randint(-50, 50)
                            aldeano["target_y"] = center_y + random.randint(-50, 50)
                            aldeano["harvesting"] = True
                            aldeano["harvest_timer"] = pygame.time.get_ticks()
                            aldeano["scale"] = 100
                            aldeano["harvest_color"] = None
                    elif button["text"] == "2. Collect Wood":  # Botón de recolectar madera
                        # Inicia acción de recolección
                        village.actions.insert(1)
                        add_to_console("Collecting wood...")
                        for lumberjack in lumberjacks:      # Configura cada leñador
                            lumberjack["target_x"] = random.randint(0, 200)
                            lumberjack["target_y"] = random.randint(0, 200)
                            lumberjack["collecting_wood"] = True
                            lumberjack["wood_timer"] = pygame.time.get_ticks()
                            lumberjack["reached_wood_point"] = False
                    elif button["text"] == "3. Mine":       # Botón de minería
                        # Inicia acción de minería
                        village.actions.insert(2)
                        add_to_console("Mining...")
                        for minero in mineros:              # Configura cada minero
                            minero["target_x"] = 1150
                            minero["target_y"] = 300
                            minero["mining"] = True
                    elif button["text"] == "4. Explore":    # Botón de exploración
                        # Inicia acción de exploración
                        village.actions.insert(3)
                        add_to_console("Exploring...")
                        for character_list in [lumberjacks, mineros, aldeanos, soldados]:
                            for character in character_list:  # Configura cada personaje
                                character["exploring"] = True
                                character["explore_phase"] = 0
                                # Asigna punto aleatorio en los bordes
                                side = random.choice(["left", "right", "top", "bottom"])
                                if side == "left":
                                    character["target_x"] = -150
                                    character["target_y"] = random.randint(0, screen_height)
                                elif side == "right":
                                    character["target_x"] = screen_width + 150
                                    character["target_y"] = random.randint(0, screen_height)
                                elif side == "top":
                                    character["target_x"] = random.randint(0, screen_width - console_width)
                                    character["target_y"] = -150
                                else:
                                    character["target_x"] = random.randint(0, screen_width - console_width)
                                    character["target_y"] = screen_height + 150
                    elif button["text"] == "5. Exit":       # Botón de salir
                        running = False                     # Termina el bucle principal
                    elif button["text"] == "6. Attack!":    # Botón de ataque
                        # Inicia estado de ataque
                        under_attack = True
                        attack_start_time = pygame.time.get_ticks()
                        add_to_console("¡La aldea está bajo ataque!")
                        # Mueve personajes civiles al centro
                        center_x = (screen_width - console_width) // 2
                        center_y = screen_height // 2
                        for character_list in [lumberjacks, mineros, aldeanos]:
                            for character in character_list:
                                character["target_x"] = center_x + random.randint(-50, 50)
                                character["target_y"] = center_y + random.randint(-50, 50)
                                character["under_attack"] = True
                                character["mining"] = False
                                character["collecting_wood"] = False
                                character["exploring"] = False
                                character["harvesting"] = False
                        
                        # Posiciona soldados en las esquinas
                        positions = [
                            (0, 0),
                            (screen_width - console_width - 100, 0),
                            (0, screen_height - 100),
                            (screen_width - console_width - 100, screen_height - 100)
                        ]
                        for i, soldado in enumerate(soldados):
                            pos = positions[i % len(positions)]
                            soldado["target_x"] = pos[0]
                            soldado["target_y"] = pos[1]
                            soldado["under_attack"] = True
                            soldado["exploring"] = False
                    elif button["text"] == "7. Execute":    # Botón de ejecutar
                        # Ejecuta acciones acumuladas
                        village.year += 1
                        village.actions.execute(village.characters)
                        add_to_console(f"Executing actions... Year: {village.year}")
        
        # Manejo de entrada por teclado
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:    # Si se presiona Enter
                if input_text.strip():          # Si hay texto ingresado
                    # Procesa comandos de texto (similar a los botones)
                    if input_text == "1":       # Comando de cosecha
                        village.actions.insert(0)
                        add_to_console("Harvesting...")
                        center_x = (screen_width - console_width) // 2
                        center_y = screen_height // 2
                        for aldeano in aldeanos:
                            aldeano["target_x"] = center_x + random.randint(-50, 50)
                            aldeano["target_y"] = center_y + random.randint(-50, 50)
                            aldeano["harvesting"] = True
                            aldeano["harvest_timer"] = pygame.time.get_ticks()
                            aldeano["scale"] = 100
                            aldeano["harvest_color"] = None
                    elif input_text == "2":     # Comando de recolectar madera
                        village.actions.insert(1)
                        add_to_console("Collecting wood...")
                        for lumberjack in lumberjacks:
                            lumberjack["target_x"] = random.randint(0, 200)
                            lumberjack["target_y"] = random.randint(0, 200)
                            lumberjack["collecting_wood"] = True
                            lumberjack["wood_timer"] = pygame.time.get_ticks()
                            lumberjack["reached_wood_point"] = False
                    elif input_text == "3":     # Comando de minería
                        village.actions.insert(2)
                        add_to_console("Mining...")
                        for minero in mineros:
                            minero["target_x"] = 1150
                            minero["target_y"] = 300
                            minero["mining"] = True
                    elif input_text == "4":     # Comando de exploración
                        village.actions.insert(3)
                        add_to_console("Exploring...")
                        for character_list in [lumberjacks, mineros, aldeanos, soldados]:
                            for character in character_list:
                                character["exploring"] = True
                                character["explore_phase"] = 0
                                side = random.choice(["left", "right", "top", "bottom"])
                                if side == "left":
                                    character["target_x"] = -150
                                    character["target_y"] = random.randint(0, screen_height)
                                elif side == "right":
                                    character["target_x"] = screen_width + 150
                                    character["target_y"] = random.randint(0, screen_height)
                                elif side == "top":
                                    character["target_x"] = random.randint(0, screen_width - console_width)
                                    character["target_y"] = -150
                                else:
                                    character["target_x"] = random.randint(0, screen_width - console_width)
                                    character["target_y"] = screen_height + 150
                    elif input_text == "5":     # Comando de salir
                        running = False
                    elif input_text == "6":     # Comando de ataque
                        under_attack = True
                        attack_start_time = pygame.time.get_ticks()
                        add_to_console("¡La aldea está bajo ataque!")
                        center_x = (screen_width - console_width) // 2
                        center_y = screen_height // 2
                        for character_list in [lumberjacks, mineros, aldeanos]:
                            for character in character_list:
                                character["target_x"] = center_x + random.randint(-50, 50)
                                character["target_y"] = center_y + random.randint(-50, 50)
                                character["under_attack"] = True
                                character["mining"] = False
                                character["collecting_wood"] = False
                                character["exploring"] = False
                                character["harvesting"] = False
                        
                        positions = [
                            (0, 0),
                            (screen_width - console_width - 100, 0),
                            (0, screen_height - 100),
                            (screen_width - console_width - 100, screen_height - 100)
                        ]
                        for i, soldado in enumerate(soldados):
                            pos = positions[i % len(positions)]
                            soldado["target_x"] = pos[0]
                            soldado["target_y"] = pos[1]
                            soldado["under_attack"] = True
                            soldado["exploring"] = False
                    else:
                        add_to_console(f"> {input_text}")
                    input_text = ""             # Limpia el texto de entrada
            elif event.key == pygame.K_BACKSPACE:  # Si se presiona Backspace
                input_text = input_text[:-1]    # Borra último carácter
            else:
                input_text += event.unicode     # Agrega carácter presionado

    # Verifica si termina el ataque
    if under_attack and pygame.time.get_ticks() - attack_start_time > 10000:  # Después de 10 segundos
        under_attack = False
        add_to_console("¡El ataque ha terminado!")
        for character_list in [lumberjacks, mineros, aldeanos, soldados]:
            for character in character_list:
                character["under_attack"] = False
                character["target_x"] = random.randint(0, screen_width - console_width)
                character["target_y"] = random.randint(0, screen_height)

    # Lógica de movimiento de personajes
    # Actualiza leñadores
    for lumberjack in lumberjacks:
        if not under_attack:
            if lumberjack["exploring"]:         # Si está explorando
                # Mueve hacia el objetivo
                lumberjack["x"], lumberjack["y"] = MovementFunctions.move_to(lumberjack["target_x"], lumberjack["target_y"], lumberjack["x"], lumberjack["y"], speed)
                if abs(lumberjack["x"] - lumberjack["target_x"]) < 10 and abs(lumberjack["y"] - lumberjack["target_y"]) < 10:
                    if lumberjack["explore_phase"] == 0:
                        lumberjack["explore_phase"] = 1
                        lumberjack["target_x"] = random.randint(0, screen_width - console_width)
                        lumberjack["target_y"] = random.randint(0, screen_height)
                    else:
                        lumberjack["exploring"] = False
            elif lumberjack["collecting_wood"]:  # Si está recolectando madera
                current_time = pygame.time.get_ticks()
                if not lumberjack["reached_wood_point"]:
                    lumberjack["x"], lumberjack["y"] = MovementFunctions.move_to(lumberjack["target_x"], lumberjack["target_y"], lumberjack["x"], lumberjack["y"], speed)
                    if abs(lumberjack["x"] - lumberjack["target_x"]) < 5 and abs(lumberjack["y"] - lumberjack["target_y"]) < 5:
                        lumberjack["reached_wood_point"] = True
                        lumberjack["wood_timer"] = pygame.time.get_ticks()
                elif current_time - lumberjack["wood_timer"] < 5000:  # Durante 5 segundos
                    lumberjack["shake_offset"] = random.randint(-2, 2)  # Efecto de temblor
                else:
                    lumberjack["collecting_wood"] = False
                    lumberjack["shake_offset"] = 0
                    lumberjack["reached_wood_point"] = False
                    lumberjack["target_x"] = random.randint(0, screen_width - console_width)
                    lumberjack["target_y"] = random.randint(0, screen_height)
            else:                               # Movimiento normal
                lumberjack["x"], lumberjack["y"] = MovementFunctions.move_to(lumberjack["target_x"], lumberjack["target_y"], lumberjack["x"], lumberjack["y"], speed)
                if abs(lumberjack["x"] - lumberjack["target_x"]) < 5 and abs(lumberjack["y"] - lumberjack["target_y"]) < 5:
                    lumberjack["target_x"] = random.randint(0, screen_width - console_width)
                    lumberjack["target_y"] = random.randint(0, screen_height)
        else:
            lumberjack["x"], lumberjack["y"] = MovementFunctions.move_to(lumberjack["target_x"], lumberjack["target_y"], lumberjack["x"], lumberjack["y"], speed)

    # Actualiza mineros
    for minero in mineros:
        if not under_attack:
            if minero["exploring"]:             # Si está explorando
                minero["x"], minero["y"] = MovementFunctions.move_to(minero["target_x"], minero["target_y"], minero["x"], minero["y"], speed)
                if abs(minero["x"] - minero["target_x"]) < 10 and abs(minero["y"] - minero["target_y"]) < 10:
                    if minero["explore_phase"] == 0:
                        minero["explore_phase"] = 1
                        minero["target_x"] = random.randint(0, screen_width - console_width)
                        minero["target_y"] = random.randint(0, screen_height)
                    else:
                        minero["exploring"] = False
            else:
                if abs(minero["x"] - minero["target_x"]) < 10 and abs(minero["y"] - minero["target_y"]) < 10:
                    if minero["mining"]:         # Si está minando
                        if minero["scale"] > 20:
                            minero["scale"] -= 2  # Efecto de reducción
                        else:
                            minero["mine_timer"] += 1
                            if minero["mine_timer"] > 60:
                                minero["scale"] = 100
                                minero["mining"] = False
                                minero["mine_timer"] = 0
                                minero["target_x"], minero["target_y"] = random.randint(0, screen_width - console_width), random.randint(0, screen_height)
                    else:
                        minero["target_x"], minero["target_y"] = random.randint(0, screen_width - console_width), random.randint(0, screen_height)
        minero["x"], minero["y"] = MovementFunctions.move_to(minero["target_x"], minero["target_y"], minero["x"], minero["y"], speed)

    # Actualiza aldeanos
    for aldeano in aldeanos:
        if not under_attack:
            if aldeano["exploring"]:            # Si está explorando
                aldeano["x"], aldeano["y"] = MovementFunctions.move_to(aldeano["target_x"], aldeano["target_y"], aldeano["x"], aldeano["y"], speed)
                if abs(aldeano["x"] - aldeano["target_x"]) < 10 and abs(aldeano["y"] - aldeano["target_y"]) < 10:
                    if aldeano["explore_phase"] == 0:
                        aldeano["explore_phase"] = 1
                        aldeano["target_x"] = random.randint(0, screen_width - console_width)
                        aldeano["target_y"] = random.randint(0, screen_height)
                    else:
                        aldeano["exploring"] = False
            elif aldeano["harvesting"]:         # Si está cosechando
                current_time = pygame.time.get_ticks()
                aldeano["x"], aldeano["y"] = MovementFunctions.move_to(aldeano["target_x"], aldeano["target_y"], aldeano["x"], aldeano["y"], speed)
                if abs(aldeano["x"] - aldeano["target_x"]) < 10 and abs(aldeano["y"] - aldeano["target_y"]) < 10:
                    if aldeano["scale"] > 40:
                        aldeano["scale"] -= 2    # Efecto de reducción
                    elif current_time - aldeano["harvest_timer"] < 3000:
                        aldeano["harvest_color"] = GREEN  # Cambia color durante cosecha
                    else:
                        aldeano["harvesting"] = False
                        aldeano["scale"] = 100
                        aldeano["harvest_color"] = None
                        aldeano["target_x"] = random.randint(0, screen_width - console_width)
                        aldeano["target_y"] = random.randint(0, screen_height)
            else:
                if abs(aldeano["x"] - aldeano["target_x"]) < 10 and abs(aldeano["y"] - aldeano["target_y"]) < 10:
                    aldeano["target_x"], aldeano["target_y"] = random.randint(0, screen_width - console_width), random.randint(0, screen_height)
        aldeano["x"], aldeano["y"] = MovementFunctions.move_to(aldeano["target_x"], aldeano["target_y"], aldeano["x"], aldeano["y"], speed)

    # Actualiza soldados
    for soldado in soldados:
        if not under_attack:
            if soldado["exploring"]:            # Si está explorando
                soldado["x"], soldado["y"] = MovementFunctions.move_to(soldado["target_x"], soldado["target_y"], soldado["x"], soldado["y"], speed)
                if abs(soldado["x"] - soldado["target_x"]) < 10 and abs(soldado["y"] - soldado["target_y"]) < 10:
                    if soldado["explore_phase"] == 0:
                        soldado["explore_phase"] = 1
                        soldado["target_x"] = random.randint(0, screen_width - console_width)
                        soldado["target_y"] = random.randint(0, screen_height)
                    else:
                        soldado["exploring"] = False
            else:
                if abs(soldado["x"] - soldado["target_x"]) < 10 and abs(soldado["y"] - soldado["target_y"]) < 10:
                    soldado["target_x"], soldado["target_y"] = random.randint(0, screen_width - console_width), random.randint(0, screen_height)
        soldado["x"], soldado["y"] = MovementFunctions.move_to(soldado["target_x"], soldado["target_y"], soldado["x"], soldado["y"], speed)

    # Renderizado de gráficos
    screen.blit(background_image, (0, 0))       # Dibuja fondo

    # Dibuja overlay rojo durante ataque
    if under_attack:
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill(RED)
        overlay.set_alpha(30)                   # Semi-transparente
        screen.blit(overlay, (0, 0))

    # Dibuja todos los personajes
    for lumberjack in lumberjacks:             # Dibuja leñadores
        screen.blit(lumberjack["image"], (lumberjack["x"] + lumberjack["shake_offset"], lumberjack["y"] + lumberjack["shake_offset"]))
    for minero in mineros:                     # Dibuja mineros
        scaled_image = pygame.transform.smoothscale(minero_image, (minero["scale"], minero["scale"]))
        screen.blit(scaled_image, (minero["x"], minero["y"]))
    for aldeano in aldeanos:                   # Dibuja aldeanos
        scaled_image = pygame.transform.smoothscale(aldeano_image, (aldeano["scale"], aldeano["scale"]))
        if aldeano["harvest_color"]:
            colored_image = scaled_image.copy()
            colored_image.fill(aldeano["harvest_color"], special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(colored_image, (aldeano["x"], aldeano["y"]))
        else:
            screen.blit(scaled_image, (aldeano["x"], aldeano["y"]))
    for soldado in soldados:
        screen.blit(soldado["image"], (soldado["x"], soldado["y"]))

    # Dibujar consola
    console_surface.fill(BLACK)
    
    # Dibujar texto de la consola
    y_offset = 10
    for text in console_text:
        text_surface = font.render(text, True, WHITE)
        console_surface.blit(text_surface, (10, y_offset))
        y_offset += 20

    # Dibujar botones en la consola
    for button in buttons:
        pygame.draw.rect(console_surface, GRAY, button["rect"].move(-screen_width + console_width, 0))
        text_surface = font.render(button["text"], True, BLACK)
        console_surface.blit(text_surface, (button["rect"].x - screen_width + console_width + 5, button["rect"].y + 10))

    # Dibujar línea de entrada en la parte inferior
    input_surface = font.render(f"> {input_text}", True, WHITE)
    console_surface.blit(input_surface, (10, console_height - 25))

    # Draw console to screen
    screen.blit(console_surface, (screen_width - console_width, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

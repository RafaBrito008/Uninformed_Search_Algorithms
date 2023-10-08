import pygame
import pygame_gui
from collections import deque

# Inicialización de pygame
pygame.init()

# Definición de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Direcciones posibles (abajo, derecha, arriba, izquierda)
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Tamaño de celda
ANCHO_CELDA = 30
ALTO_CELDA = 30
GROSOR_PARED = 8

# Tamaño del laberinto
ANCHO_LABERINTO = 31
ALTO_LABERINTO = 21

# Ajustar las dimensiones de la ventana para incluir el margen superior
MARGEN_SUPERIOR = 60
ANCHO_VENTANA = ANCHO_LABERINTO * ANCHO_CELDA
ALTO_VENTANA = ALTO_LABERINTO * ALTO_CELDA + MARGEN_SUPERIOR

# Fuente para dibujar números
font = pygame.font.SysFont(None, 25)

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Depth First Search")

# Laberinto definido como una matriz
laberinto = [
    "################################",
    "#I                            #",
    "# ##################### ##### #",
    "#     #               #     # #",
    "# ### # ############# ### # # #",
    "# #   # #           # #   # # #",
    "# # ### # ######### # # # # # #",
    "# #     #         # # # #   # #",
    "# ############### # # # ##### #",
    "#               # # # #       #",
    "############# ### # # #########",
    "#             #   # #         #",
    "# ########### ### # ######### #",
    "# #           #     #       # #",
    "# # ######### ##### ####### # #",
    "# #       # #               # #",
    "# ####### # # ############### #",
    "#       # # #                 #",
    "####### # # ############### ###",
    "#         #               #  O#",
    "###############################"
]

def dibujar_laberinto():
    for fila in range(ALTO_LABERINTO):
        for columna in range(ANCHO_LABERINTO):
            x = columna * ANCHO_CELDA
            y = fila * ALTO_CELDA + MARGEN_SUPERIOR  # Ajustar la posición en y considerando el margen
            if laberinto[fila][columna] == "#":
                pygame.draw.rect(ventana, NEGRO, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif laberinto[fila][columna] == "I":
                pygame.draw.rect(ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif laberinto[fila][columna] == "O":
                pygame.draw.rect(ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA), GROSOR_PARED) 
            else:
                pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CELDA, ALTO_CELDA))


def iddfs(laberinto, inicio, objetivo):
    for profundidad_maxima in range(1, len(laberinto) * len(laberinto[0])):
        resultado, nodos_visitados = depth_limited_dfs(laberinto, inicio, objetivo, profundidad_maxima)
        if resultado is not None:
            return resultado, nodos_visitados
    return [], nodos_visitados

def depth_limited_dfs(laberinto, inicio, objetivo, profundidad_maxima):
    stack = deque()
    visitado = set()
    camino = {}
    stack.append((inicio, 0))
    visitado.add(inicio)

    nodos_visitados = []

    while stack:
        nodo, profundidad = stack.pop()
        nodos_visitados.append(nodo)

        if profundidad > profundidad_maxima:
            continue

        if nodo == objetivo:
            ruta = []
            while nodo in camino:
                ruta.append(nodo)
                nodo = camino[nodo]
            ruta.append(inicio)
            return ruta[::-1], nodos_visitados

        for dx, dy in reversed(DIRS):
            x, y = nodo
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)
            if (0 <= nx < len(laberinto[0]) and 0 <= ny < len(laberinto)
                and laberinto[ny][nx] != "#"
                and vecino not in visitado):
                stack.append((vecino, profundidad + 1))
                visitado.add(vecino)
                camino[vecino] = nodo

    return None, nodos_visitados



def main():
    inicio = None
    objetivo = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == "I":
                inicio = (x, y)
            elif celda == "O":
                objetivo = (x, y)

    solucion = []
    nodos_visitados = []

    manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))
    boton_inicio = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((ANCHO_VENTANA//2 - 75, 10), (150, 40)),
                                                text='Buscar Solución',
                                                manager=manager)

    corriendo = True
    while corriendo:
        tiempo_transcurrido = pygame.time.Clock().tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            manager.process_events(evento)

            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == boton_inicio:
                        solucion, nodos_visitados = iddfs(laberinto, inicio, objetivo)  # Cambiar aquí

        ventana.fill(BLANCO)
        dibujar_laberinto()
        
        if solucion:
            for (x, y) in solucion:
                pygame.draw.rect(ventana, VERDE, (x * ANCHO_CELDA, y * ALTO_CELDA + MARGEN_SUPERIOR, ANCHO_CELDA, ALTO_CELDA))

        paso = 0
        for (x, y) in nodos_visitados:
            texto = font.render(str(paso), True, NEGRO)
            ventana.blit(texto, (x * ANCHO_CELDA + 5, y * ALTO_CELDA + 5 + MARGEN_SUPERIOR))
            paso += 1
        
        manager.update(tiempo_transcurrido)
        manager.draw_ui(ventana)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
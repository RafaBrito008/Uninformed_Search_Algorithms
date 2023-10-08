import pygame
import pygame_gui
from collections import deque

pygame.init()

# Definición de colores y direcciones
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Acciones que puede tomar el agente
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # ARRIBA, DERECHA, ABAJO, IZQUIERDA

#Elementos visuales
ANCHO_CELDA = 30
ALTO_CELDA = 25
GROSOR_PARED = 8
ANCHO_LABERINTO = 31
ALTO_LABERINTO = 31
MARGEN_SUPERIOR = 60
ANCHO_VENTANA = ANCHO_LABERINTO * ANCHO_CELDA
ALTO_VENTANA = ALTO_LABERINTO * ALTO_CELDA + MARGEN_SUPERIOR

# Laberinto y otros recursos visuales
font = pygame.font.SysFont(None, 22)
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Depth First Search")

laberinto = [
    "###############################",
    "#I#     #   #     #           #",
    "# # ### # ### # ### ### # ### #",
    "# #   # # #   #  #  #   #     #",
    "# ### # # # ### ### # ### ### #",
    "#   #   # #   #       #       #",
    "# ### ### ##### # ########### #",
    "#     # # #     # # #       # #",
    "# ##### # # ####### # ### ### #",
    "#       #   #   #   # #   #   #",
    "### # # # ##### # ### # # # # #",
    "#   # #               # #   # #",
    "# # # ### # ### ####### ##### #",
    "# # #     #   #     # #       #",
    "### # ### # # ### # # #########",
    "#       #   #     #   #     # #",
    "# # ### ### ### ### # # ### # #",
    "# #             #   #   # #   #",
    "# # ####### # ### # ##### # # #",
    "#   #       #     #         # #",
    "# ### # # ### ### # ######### #",
    "#     # #       #           # #",
    "# ##### # ### # ##### ### # # #",
    "#     #       #     # #   #   #",
    "# # # # # # ### # # # # # ### #",
    "# # #   # # #   # #     #   # #",
    "# # # ### # # ### # ### # # # #",
    "#     #         #   #     #   #",
    "# ### # ##### # # ### ### ### #",
    "#       #     #       #      O#",
    "###############################",
]


def dibujar_laberinto():
    for fila in range(ALTO_LABERINTO):
        for columna in range(ANCHO_LABERINTO):
            x = columna * ANCHO_CELDA
            y = fila * ALTO_CELDA + MARGEN_SUPERIOR
            char = laberinto[fila][columna]
            color = {
                "#": NEGRO,
                "I": VERDE,
                "O": VERDE,
                " ": BLANCO
            }.get(char, BLANCO)
            pygame.draw.rect(ventana, color, (x, y, ANCHO_CELDA, ALTO_CELDA))
            if char == "O":
                pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CELDA, ALTO_CELDA), GROSOR_PARED)

def dfs(laberinto, inicio, objetivo):
    stack = deque([inicio])
    visitado = set([inicio])
    camino = {}
    nodos_visitados = []
    
    while stack:
        nodo = stack.pop()
        nodos_visitados.append(nodo)

        if nodo == objetivo:
            ruta = []
            while nodo in camino:
                ruta.append(nodo)
                nodo = camino[nodo]
            ruta.append(inicio)
            return ruta[::-1], nodos_visitados
        
        for dx, dy in DIRS:
            x, y = nodo
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)
            if (
                0 <= nx < ANCHO_LABERINTO
                and 0 <= ny < ALTO_LABERINTO
                and laberinto[ny][nx] != "#"
                and vecino not in visitado
            ):
                stack.append(vecino)
                visitado.add(vecino)
                camino[vecino] = nodo
    return [], nodos_visitados

def main():
    inicio = None
    objetivo = None
    for y, fila in enumerate(laberinto):
        for x, char in enumerate(fila):
            if char == "I":
                inicio = (x, y)
            elif char == "O":
                objetivo = (x, y)

    solucion = []
    nodos_visitados = []

    manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))
    boton_inicio = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO_VENTANA // 2 - 75, 10), (150, 40)),
        text="Buscar Solución",
        manager=manager
    )

    corriendo = True
    while corriendo:
        tiempo_transcurrido = pygame.time.Clock().tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            manager.process_events(evento)
            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED and evento.ui_element == boton_inicio:
                    solucion, nodos_visitados = dfs(laberinto, inicio, objetivo)

        ventana.fill(BLANCO)
        dibujar_laberinto()

        for x, y in solucion:
            pygame.draw.rect(ventana, VERDE, (x * ANCHO_CELDA, y * ALTO_CELDA + MARGEN_SUPERIOR, ANCHO_CELDA, ALTO_CELDA))

        for paso, (x, y) in enumerate(nodos_visitados):
            texto = font.render(str(paso), True, NEGRO)
            ventana.blit(texto, (x * ANCHO_CELDA + 5, y * ALTO_CELDA + 5 + MARGEN_SUPERIOR))

        manager.update(tiempo_transcurrido)
        manager.draw_ui(ventana)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
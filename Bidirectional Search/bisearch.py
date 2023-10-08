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
ANCHO_CELDA = 40
ALTO_CELDA = 30
GROSOR_PARED = 8

# Tamaño del laberinto
ANCHO_LABERINTO = 31
ALTO_LABERINTO = 31

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
    "###############################",
    "#I#     #   #     #           #",
    "# # ### # ### # ### ### # ### #",
    "# #   # # #   #  #  #   #     #",
    "# ### # # # ### ### # ### ### #",
    "#   #   # #           #       #",
    "# ### ### ##### # ########### #",
    "#     # # #     # #           #",
    "# ##### # # ### ### # ### ### #",
    "#       #   #   #   #     #   #",
    "### # # # ##### # ### # # # # #",
    "#   # #               # #   # #",
    "# # # ### # ### ####### ##### #",
    "# # #     #   #     #         #",
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
            y = (
                fila * ALTO_CELDA + MARGEN_SUPERIOR
            )  # Ajustar la posición en y considerando el margen
            if laberinto[fila][columna] == "#":
                pygame.draw.rect(ventana, NEGRO, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif laberinto[fila][columna] == "I":
                pygame.draw.rect(ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif laberinto[fila][columna] == "O":
                pygame.draw.rect(
                    ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA), GROSOR_PARED
                )
            else:
                pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CELDA, ALTO_CELDA))


def bidirectional_search(laberinto, inicio, objetivo):
    forward_queue = deque()
    backward_queue = deque()
    forward_visited = set()
    backward_visited = set()
    forward_parent = {}
    backward_parent = {}

    forward_queue.append(inicio)
    forward_visited.add(inicio)
    backward_queue.append(objetivo)
    backward_visited.add(objetivo)

    intersect_node = None

    forward_nodos_en_orden = (
        []
    )  # Lista para guardar el orden de los nodos visitados desde el inicio
    backward_nodos_en_orden = (
        []
    )  # Lista para guardar el orden de los nodos visitados desde el final

    while forward_queue and backward_queue:
        # Búsqueda hacia adelante
        forward_node = forward_queue.popleft()
        forward_nodos_en_orden.append(forward_node)  # Agregar nodo a la lista de orden
        for dx, dy in reversed(DIRS):
            x, y = forward_node
            nx, ny = x + dx, y + dy
            forward_neighbor = (nx, ny)
            if (
                0 <= nx < len(laberinto[0])
                and 0 <= ny < len(laberinto)
                and laberinto[ny][nx] != "#"
                and forward_neighbor not in forward_visited
            ):
                forward_queue.append(forward_neighbor)
                forward_visited.add(forward_neighbor)
                forward_parent[forward_neighbor] = forward_node

                if forward_neighbor in backward_visited:
                    intersect_node = forward_neighbor
                    break

        if intersect_node:
            break

        # Búsqueda hacia atrás
        backward_node = backward_queue.popleft()
        backward_nodos_en_orden.append(
            backward_node
        )  # Agregar nodo a la lista de orden
        for dx, dy in reversed(DIRS):
            x, y = backward_node
            nx, ny = x + dx, y + dy
            backward_neighbor = (nx, ny)
            if (
                0 <= nx < len(laberinto[0])
                and 0 <= ny < len(laberinto)
                and laberinto[ny][nx] != "#"
                and backward_neighbor not in backward_visited
            ):
                backward_queue.append(backward_neighbor)
                backward_visited.add(backward_neighbor)
                backward_parent[backward_neighbor] = backward_node

                if backward_neighbor in forward_visited:
                    intersect_node = backward_neighbor
                    break

        if intersect_node:
            break

    if not intersect_node:
        return [], []

    # Reconstruir el camino
    forward_path = []
    node = intersect_node
    while node != inicio:
        forward_path.append(node)
        node = forward_parent[node]
    forward_path.reverse()

    backward_path = []
    node = intersect_node
    while node != objetivo:
        backward_path.append(node)
        node = backward_parent[node]

    return (
        forward_path + [intersect_node] + backward_path,
        forward_nodos_en_orden,
        backward_nodos_en_orden,
    )


def main():
    inicio = None
    objetivo = None
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == "I":
                inicio = (x, y)
            elif celda == "O":
                objetivo = (x, y)

    solucion, forward_nodos_en_orden, backward_nodos_en_orden = [], [], []
    manager = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA))
    boton_inicio = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO_VENTANA // 2 - 75, 10), (150, 40)),
        text="Buscar Solución",
        manager=manager,
    )

    corriendo = True
    while corriendo:
        tiempo_transcurrido = pygame.time.Clock().tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            manager.process_events(evento)

            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == boton_inicio:
                    (
                        solucion,
                        forward_nodos_en_orden,
                        backward_nodos_en_orden,
                    ) = bidirectional_search(laberinto, inicio, objetivo)

        ventana.fill(BLANCO)
        dibujar_laberinto()

        if solucion:
            for x, y in solucion:
                pygame.draw.rect(
                    ventana,
                    VERDE,
                    (
                        x * ANCHO_CELDA,
                        y * ALTO_CELDA + MARGEN_SUPERIOR,
                        ANCHO_CELDA,
                        ALTO_CELDA,
                    ),
                )

        for x, y in forward_nodos_en_orden:
            indice = forward_nodos_en_orden.index((x, y))
            texto = font.render(f"I{indice}", True, NEGRO)
            ventana.blit(
                texto, (x * ANCHO_CELDA + 5, y * ALTO_CELDA + 5 + MARGEN_SUPERIOR)
            )

        for x, y in backward_nodos_en_orden:
            indice = backward_nodos_en_orden.index((x, y))
            texto = font.render(f"F{indice}", True, NEGRO)
            ventana.blit(
                texto, (x * ANCHO_CELDA + 5, y * ALTO_CELDA + 5 + MARGEN_SUPERIOR)
            )

        manager.update(tiempo_transcurrido)
        manager.draw_ui(ventana)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import pygame_gui
from collections import deque

# Importar el laberinto
import sys

sys.path.append("./")
from laberinto import *

# Inicialización de pygame
pygame.init()

# Acciones que puede tomar el agente
ACCIONES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # ARRIBA, DERECHA, ABAJO, IZQUIERDA


def iddfs(laberinto, inicio, objetivo):
    for profundidad_maxima in range(1, len(laberinto) * len(laberinto[0])):
        resultado, nodos_visitados = depth_limited_dfs(
            laberinto, inicio, objetivo, profundidad_maxima
        )
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

        for dx, dy in ACCIONES:
            x, y = nodo
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)
            if (
                0 <= nx < len(laberinto[0])
                and 0 <= ny < len(laberinto)
                and laberinto[ny][nx] != "#"
                and vecino not in visitado
            ):
                stack.append((vecino, profundidad + 1))
                visitado.add(vecino)
                camino[vecino] = nodo

    return None, nodos_visitados


def main():
    # Fuente para dibujar números
    font = pygame.font.SysFont(None, 22)

    # Crear la ventana
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Iterative Deepening Depth-First Search")

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

            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == boton_inicio:
                        solucion, nodos_visitados = iddfs(
                            laberinto, inicio, objetivo
                        )  # Cambiar aquí

        ventana.fill(BLANCO)
        dibujar_laberinto(ventana)

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

        paso = 0
        for x, y in nodos_visitados:
            texto = font.render(str(paso), True, NEGRO)
            ventana.blit(
                texto, (x * ANCHO_CELDA + 5, y * ALTO_CELDA + 5 + MARGEN_SUPERIOR)
            )
            paso += 1

        manager.update(tiempo_transcurrido)
        manager.draw_ui(ventana)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

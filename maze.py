import pygame

# Inicialización de pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)

# Tamaño de celda y pared
ANCHO_CELDA = 20
ALTO_CELDA = 20
GROSOR_PARED = 5

# Dimensiones de la ventana
ANCHO_VENTANA = 31 * ANCHO_CELDA
ALTO_VENTANA = 21 * ALTO_CELDA

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto")

# Laberinto definido como una matriz
laberinto = [
    # Aquí solo hay un ejemplo simple de laberinto, puedes modificarlo según necesites
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
    for fila in range(21):
        for columna in range(31):
            x = columna * ANCHO_CELDA
            y = fila * ALTO_CELDA
            if laberinto[fila][columna] == "#":
                pygame.draw.rect(ventana, NEGRO, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif laberinto[fila][columna] == "I":
                pygame.draw.rect(ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA))
            elif laberinto[fila][columna] == "O":
                pygame.draw.rect(ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA), GROSOR_PARED) # Borde verde para la salida
            else:
                pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CELDA, ALTO_CELDA))

# Bucle principal del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    ventana.fill(BLANCO)
    dibujar_laberinto()
    pygame.display.flip()

pygame.quit()

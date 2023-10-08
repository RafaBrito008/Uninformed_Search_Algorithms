import pygame

# Definición de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

#Elementos visuales
ANCHO_CELDA = 30
ALTO_CELDA = 25
GROSOR_PARED = 8
ANCHO_LABERINTO = 31
ALTO_LABERINTO = 31
MARGEN_SUPERIOR = 60
ANCHO_VENTANA = ANCHO_LABERINTO * ANCHO_CELDA
ALTO_VENTANA = ALTO_LABERINTO * ALTO_CELDA + MARGEN_SUPERIOR

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

def dibujar_laberinto(ventana):
    for fila in range(ALTO_LABERINTO):
        for columna in range(ANCHO_LABERINTO):
            x = columna * ANCHO_CELDA
            y = fila * ALTO_CELDA + MARGEN_SUPERIOR
            char = laberinto[fila][columna]
            color = {
                "#": NEGRO,
                "I": VERDE,
                "O": BLANCO,
                " ": BLANCO
            }.get(char, BLANCO)
            pygame.draw.rect(ventana, color, (x, y, ANCHO_CELDA, ALTO_CELDA))
            if char == "O":
                pygame.draw.rect(ventana, ROJO, (x, y, ANCHO_CELDA, ALTO_CELDA), GROSOR_PARED)
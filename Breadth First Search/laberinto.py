import tkinter as tk
from tkinter import messagebox
from collections import deque
from queue import Queue

GRID_SIZE = 40
GRID_WIDTH = 8
GRID_HEIGHT = 8
WINDOW_SIZE = (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)

WHITE = "white"
BLACK = "black"
RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"


class TreeNode:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent


def build_tree(start, goal, obstacles):
    root = TreeNode(start[0], start[1])
    queue = Queue()
    queue.put(root)

    explored = set()

    while not queue.empty():
        node = queue.get()
        x, y = node.x, node.y

        if (x, y) == goal:
            return node

        if (x, y) in explored:
            continue

        explored.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if (new_x, new_y) not in obstacles:
                    child = TreeNode(new_x, new_y, node)
                    queue.put(child)

    return None


class GridGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Búsqueda")
        self.canvas = tk.Canvas(
            root, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1], bg=WHITE
        )
        self.canvas.pack()
        self.start_node = None
        self.goal_node = None
        self.obstacles = set()

        self.searching = False
        self.path = []

        self.create_grid()

        self.search_button = tk.Button(root, text="Buscar", command=self.search)
        self.search_button.pack()

        self.clear_button = tk.Button(root, text="Limpiar", command=self.clear)
        self.clear_button.pack()

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

    def create_grid(self):
        for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
            self.canvas.create_line(x, 0, x, GRID_HEIGHT * GRID_SIZE, fill=WHITE)
        for y in range(0, GRID_HEIGHT * GRID_SIZE, GRID_SIZE):
            self.canvas.create_line(0, y, GRID_WIDTH * GRID_SIZE, y, fill=WHITE)

    def draw_rectangle(self, color, x, y):
        self.canvas.create_rectangle(
            x * GRID_SIZE,
            y * GRID_SIZE,
            (x + 1) * GRID_SIZE,
            (y + 1) * GRID_SIZE,
            fill=color,
        )

    def left_click(self, event):
        x, y = event.x // GRID_SIZE, event.y // GRID_SIZE
        if not self.start_node:
            self.start_node = (x, y)
            self.draw_rectangle(RED, x, y)
        elif not self.goal_node:
            self.goal_node = (x, y)
            self.draw_rectangle(GREEN, x, y)
        else:
            self.obstacles.add((x, y))
            self.draw_rectangle(BLUE, x, y)

    def right_click(self, event):
        x, y = event.x // GRID_SIZE, event.y // GRID_SIZE
        if (x, y) in self.obstacles:
            self.obstacles.remove((x, y))
            self.canvas.create_rectangle(
                x * GRID_SIZE,
                y * GRID_SIZE,
                (x + 1) * GRID_SIZE,
                (y + 1) * GRID_SIZE,
                fill=WHITE,
            )

    def search(self):
        if self.start_node and self.goal_node:
            self.searching = True
            goal_node = build_tree(self.start_node, self.goal_node, self.obstacles)
            if goal_node:
                self.path = self.reconstruct_path(goal_node)
                if self.path:
                    cost = len(self.path) - 1
                    self.draw_path()
                    messagebox.showinfo(
                        "Resultado de la búsqueda",
                        f"Camino encontrado con costo {cost}",
                    )

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append((node.x, node.y))
            node = node.parent
        return path[::-1]

    def draw_path(self):
        for x, y in self.path:
            if (x, y) != self.start_node and (x, y) != self.goal_node:
                self.draw_rectangle(YELLOW, x, y)
        self.root.update()

    def clear(self):
        self.start_node = None
        self.goal_node = None
        self.obstacles.clear()
        self.searching = False
        self.path = []
        self.canvas.delete("all")
        self.create_grid()


if __name__ == "__main__":
    root = tk.Tk()
    game = GridGame(root)
    root.mainloop()
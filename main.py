import tkinter as tk
import random
import time

CELL = 20
W, H = 21, 21
DELAY = 0.05

class Maze:
    def __init__(self):
        self.grid = []
        for i in range(H):
            row = []
            for j in range(W):
                row.append(1)
            self.grid.append(row)
        self._gen(0, 0)

        self.start = self.random_inner_cell()
        
        self.exits = [self.random_edge_cell() for _ in range(3)]

        sx, sy = self.start
        self.grid[sy][sx] = 0
        for ex, ey in self.exits:
            self.grid[ey][ex] = 0

    def _gen(self, x, y):
        self.grid[y][x] = 0
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(dirs)
        for d in dirs:
            dx, dy = d
            nx = x + dx * 2
            ny = y + dy * 2
            if 0 <= nx < W and 0 <= ny < H:
                if self.grid[ny][nx] == 1:
                    self.grid[y + dy][x + dx] = 0
                    self._gen(nx, ny)

    def random_edge_cell(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return (random.randrange(0, W, 2), 0)
        elif side == "bottom":
            return (random.randrange(0, W, 2), H - 1)
        elif side == "left":
            return (0, random.randrange(0, H, 2))
        else:
            return (W - 1, random.randrange(0, H, 2))

    def random_inner_cell(self):
        while True:
            x = random.randrange(1, W - 1)
            y = random.randrange(1, H - 1)
            if self.grid[y][x] == 0:
                return (x, y)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("тараканьи бега")
        self.c = tk.Canvas(root, width=W * CELL, height=H * CELL, bg="white")
        self.c.pack()
        self.mz = Maze()
        self.draw()
        self.vis = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(False)
            self.vis.append(row)
        sx, sy = self.mz.start
        self.bug = self.c.create_oval(sx * CELL + 5, sy * CELL + 5,
                                      sx * CELL + 15, sy * CELL + 15,
                                      fill="orange", outline="brown")
        self.dfs(sx, sy)

    def draw(self):
        for y in range(H):
            for x in range(W):
                val = self.mz.grid[y][x]
                if val == 1:
                    color = "black"
                else:
                    color = "white"
                x1 = x * CELL
                y1 = y * CELL
                x2 = (x + 1) * CELL
                y2 = (y + 1) * CELL
                self.c.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        sx, sy = self.mz.start
        self.c.create_rectangle(sx * CELL, sy * CELL, (sx + 1) * CELL, (sy + 1) * CELL, fill="green")
        for ex, ey in self.mz.exits:
            self.c.create_rectangle(ex * CELL, ey * CELL, (ex + 1) * CELL, (ey + 1) * CELL, fill="red")

    def move(self, x, y):
        x1 = x * CELL + 5
        y1 = y * CELL + 5
        x2 = x * CELL + 15
        y2 = y * CELL + 15
        self.c.coords(self.bug, x1, y1, x2, y2)
        self.c.tag_raise(self.bug)
        self.root.update()
        time.sleep(DELAY)

    def dfs(self, x, y):
        if not (0 <= x < W and 0 <= y < H):
            return False
        if self.mz.grid[y][x] == 1:
            return False
        if self.vis[y][x]:
            return False
        self.vis[y][x] = True
        self.move(x, y)
        if (x, y) in self.mz.exits:
            self.c.itemconfig(self.bug, fill="blue")
            return True
        self.c.create_rectangle(
            x * CELL, y * CELL, (x + 1) * CELL, (y + 1) * CELL,
            fill="#ffb366", outline=""
        )
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if self.dfs(nx, ny):
                return True
        self.move(x, y)
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

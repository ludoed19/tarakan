import tkinter as tk
import random
import time

CELL = 20
W, H = 21, 21
DELAY = 0.05

class Maze:
    def __init__(self):
        self.grid = [[1]*W for _ in range(H)]
        self._gen(0, 0)

    def _gen(self, x, y):
        self.grid[y][x] = 0
        dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx*2, y+dy*2
            if 0 <= nx < W and 0 <= ny < H and self.grid[ny][nx] == 1:
                self.grid[y+dy][x+dx] = 0
                self._gen(nx, ny)

class App:
    def __init__(self, root):
        self.root = root
        self.c = tk.Canvas(root, width=W*CELL, height=H*CELL, bg="white")
        self.c.pack()
        self.mz = Maze()
        self.draw()
        self.vis = [[False]*W for _ in range(H)]
        self.bug = self.c.create_oval(5,5,15,15,fill="orange",outline="brown")
        self.dfs(0,0)

    def draw(self):
        for y in range(H):
            for x in range(W):
                color = "black" if self.mz.grid[y][x] else "white"
                self.c.create_rectangle(x*CELL, y*CELL, (x+1)*CELL, (y+1)*CELL, fill=color, outline="")
        self.c.create_rectangle(0,0,CELL,CELL,fill="green")
        self.c.create_rectangle((W-1)*CELL,(H-1)*CELL,W*CELL,H*CELL,fill="red")

    def move(self, x, y):
        self.c.coords(self.bug, x*CELL+5, y*CELL+5, x*CELL+15, y*CELL+15)
        self.c.tag_raise(self.bug)
        self.root.update()
        time.sleep(DELAY)

    def dfs(self, x, y):
        if not (0<=x<W and 0<=y<H) or self.mz.grid[y][x] or self.vis[y][x]:
            return False
        self.vis[y][x] = True
        self.move(x, y)

        if (x, y) == (W-1, H-1):
            self.c.itemconfig(self.bug, fill="blue")
            return True

        self.c.create_rectangle(x*CELL, y*CELL, (x+1)*CELL, (y+1)*CELL, fill="#ffb366", outline="")

        for dx, dy in random.sample([(0,1),(1,0),(0,-1),(-1,0)], 4):
            if self.dfs(x+dx, y+dy):
                return True

        self.move(x, y)
        return False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("тараканьи бега")
    app = App(root)
    root.mainloop()

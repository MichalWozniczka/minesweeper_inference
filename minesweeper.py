from tkinter import *
import ImageTk
from PIL import Image
import random
import Queue

class minesweeperGui():
    def __init__(self, w, h, ms):
        self.window = Tk()
	self.canvas = Canvas(self.window, width=w, height=h, bg='#bdbdbd')
	self.canvas.pack()

        playH = h - 50
	self.tileSize = min(w/ms.width, playH/ms.height)

	self.spritesheet = Image.open('assets/sprites.png')
	self.beliefsheet = Image.open('assets/beliefs.png')

        self.numbers = [ImageTk.PhotoImage(self.spritesheet.crop((i*13, 0, (i+1)*13, 23)).resize((20, 35))) for i in range(12)]

        self.sprites = []
	for i in range(2):
	    for j in range(9):
	       self.sprites.append(ImageTk.PhotoImage(self.spritesheet.crop((j*16, 23+i*16, (j+1)*16, 23+(i+1)*16)).resize((self.tileSize, self.tileSize))))

	self.opened = [self.sprites[i] for i in range(9)]
	self.unopened = self.sprites[9]
	self.beliefs = [self.unopened]
	for i in range(20):
	    self.beliefs.append(ImageTk.PhotoImage(self.beliefsheet.crop((i*16, 0, (i+1)*16, 16)).resize((self.tileSize, self.tileSize))))
	self.flag = self.sprites[10]
	self.explodedMine = self.sprites[11]
	self.wrongMine = self.sprites[12]
	self.mine = self.sprites[13]

	self.offsx = self.tileSize/2 + (w - ms.width*self.tileSize)/2
	self.offsy = self.tileSize/2 + (playH - ms.height*self.tileSize)/2 + 50

	for i in range(ms.height):
	    for j in range(ms.width):
    		self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.unopened)

	self.canvas.create_image(self.offsx+10, 25, image=self.numbers[ms.numMines/100])
	self.canvas.create_image(self.offsx+30, 25, image=self.numbers[(ms.numMines - (ms.numMines/100)*100)/10])
	self.canvas.create_image(self.offsx+50, 25, image=self.numbers[ms.numMines - (ms.numMines/10)*10])

    def draw(self, ms, displayBeliefs=True):
        for i in range(ms.height):
	    for j in range(ms.width):
	        if ms.flipped[i][j]:
		    if ms.grid[i][j] == -2:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.explodedMine)
		    elif ms.grid[i][j] == -1:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
	            else:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.opened[ms.grid[i][j]])
		elif displayBeliefs:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.beliefs[int(ms.beliefs[i][j]*20)])
		else:
    		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.unopened)

	self.canvas.create_image(self.offsx+10, 25, image=self.numbers[ms.numMines/100])
	self.canvas.create_image(self.offsx+30, 25, image=self.numbers[(ms.numMines - (ms.numMines/100)*100)/10])
	self.canvas.create_image(self.offsx+50, 25, image=self.numbers[ms.numMines - (ms.numMines/10)*10])
		    

class minesweeper():
    def __init__(self, w, h, numMines):
        self.grid = [[0 for i in range(w)] for j in range(h)]
	self.flipped = [[False for i in range(w)] for j in range(h)]
	self.beliefs = [[float(numMines)/(w*h) for i in range(w)] for j in range(h)]
	self.width = w
	self.height = h
	self.numMines = numMines

	for i in range(numMines):
	    randCoord = (random.randrange(h), random.randrange(w))
	    while self.grid[randCoord[0]][randCoord[1]] == -2:
	        randCoord = (random.randrange(w), random.randrange(h))
	    self.grid[randCoord[0]][randCoord[1]] = -2

	for i in range(h):
	    for j in range(w):
	        if self.grid[i][j] == -2:
		    continue
	        for a in range(-1, 2):
		    for b in range(-1, 2):
		        if i+a < 0 or i+a >= h or j+b < 0 or j+b >= w:
			    continue
			self.grid[i][j] += 1 if self.grid[i+a][j+b] == -2 else 0

    def flip(self, x, y):
        self.flipped[x][y] = True
	curpos = (x, y)
        queue = Queue.Queue()
	queue.put(curpos)
	visited = set()
	while not queue.empty():
	    curpos = queue.get()
	    if curpos in visited:
	      continue
	    visited.add(curpos)
            for a in range(-1, 2):
	        for b in range(-1, 2):
		    if curpos[0]+a < 0 or curpos[0]+a >= self.height or curpos[1]+b < 0 or curpos[1]+b >= self.height:
		        continue
		    self.flipped[curpos[0]+a][curpos[1]+b] = True
		    if self.grid[curpos[0]+a][curpos[1]+b] == 0:
               	        queue.put((curpos[0]+a, curpos[1]+b))

def main():  
    ms = minesweeper(30, 30, 50)
    gui = minesweeperGui(500, 500, ms)
    ms.flip(0, 0)

    while(1):
        #gui.displayBeliefs(ms)
	gui.draw(ms)
        gui.window.update()

if __name__ == "__main__": main()
    

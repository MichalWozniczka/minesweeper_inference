from tkinter import *
import ImageTk
from PIL import Image
import random
import Queue
import time

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
        self.canvas.delete("all")
        for i in range(ms.height):
	    for j in range(ms.width):
		if not ms.flipped[i][j] and ms.flags[i][j]:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
	        elif ms.flipped[i][j]:
		    if ms.grid[i][j] == -2:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.explodedMine)
		    elif ms.grid[i][j] == -1:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
	            else:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.opened[ms.grid[i][j]])
		elif ms.beliefs[i][j] == 0:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
		elif displayBeliefs:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.beliefs[int((ms.antibeliefs[i][j])*19)])
		else:
    		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.unopened)

	self.canvas.create_image(self.offsx+10, 25, image=self.numbers[ms.numMines/100])
	self.canvas.create_image(self.offsx+30, 25, image=self.numbers[(ms.numMines - (ms.numMines/100)*100)/10])
	self.canvas.create_image(self.offsx+50, 25, image=self.numbers[ms.numMines - (ms.numMines/10)*10])

    def lossScreen(self, ms, displayBeliefs=True):
        self.canvas.delete("all")
        for i in range(ms.height):
	    for j in range(ms.width):
		if not ms.flipped[i][j] and ms.flags[i][j]:
		    if ms.grid[i][j] == -2:
  		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
		    else:
  		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.wrongMine)
	        elif ms.grid[i][j] == -2:
                    if ms.flipped[i][j]:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.explodedMine)
	            else:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.mine)
	        elif ms.flipped[i][j]:
		    if ms.grid[i][j] == -1:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
	            else:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.opened[ms.grid[i][j]])
		elif displayBeliefs:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.beliefs[int((ms.antibeliefs[i][j])*19)])
		else:
    		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.unopened)

	self.canvas.create_image(self.offsx+10, 25, image=self.numbers[ms.numMines/100])
	self.canvas.create_image(self.offsx+30, 25, image=self.numbers[(ms.numMines - (ms.numMines/100)*100)/10])
	self.canvas.create_image(self.offsx+50, 25, image=self.numbers[ms.numMines - (ms.numMines/10)*10])
		    

class minesweeper():
    def __init__(self, w, h, numMines):
        self.grid = [[0 for i in range(w)] for j in range(h)]
	self.flipped = [[False for i in range(w)] for j in range(h)]
	self.beliefs = [[1 - float(numMines)/(w*h) for i in range(w)] for j in range(h)]
	self.antibeliefs = [[float(numMines)/(w*h) for i in range(w)] for j in range(h)]
	self.flags = [[False for i in range(w)] for j in range(h)]
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
	    self.flipped[curpos[0]][curpos[1]] = True
            for a in range(-1, 2):
	        for b in range(-1, 2):
		    if curpos[0]+a < 0 or curpos[0]+a >= self.height or curpos[1]+b < 0 or curpos[1]+b >= self.height or self.grid[curpos[0]][curpos[1]] != 0:
		        continue
		    self.flipped[curpos[0]+a][curpos[1]+b] = True
		    if self.grid[curpos[0]+a][curpos[1]+b] == 0:
               	        queue.put((curpos[0]+a, curpos[1]+b))

    def unflippedTiles(self):
        cnt = 0
	for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j] == False:
		    cnt += 1

	return cnt

    def actOnNeighbors(self, x, y):
        unflippedNeighborCount = 0
	flagCount = 0
	allFlagCount = 0
	newFlagCount = 0
	neighbors = []

        for a in range(-1, 2):
	    for b in range(-1, 2):
	        if x+a < 0 or x+a >= self.height or y+b < 0 or y+b >= self.width:
		    continue
		if not self.flipped[x+a][y+b]:
		    unflippedNeighborCount += 1
		    if self.flags[x+a][y+b] or self.beliefs[x+a][y+b] == 0:
		        flagCount += 1
		    neighbors.append((x+a, y+b))

	for i in range(self.height):
	    for j in range(self.width):
	        if not self.flipped[i][j] and self.beliefs[i][j] == 0:
		    allFlagCount += 1

        for a in range(-1, 2):
	    for b in range(-1, 2):
	        if x+a < 0 or x+a >= self.height or y+b < 0 or y+b >= self.width:
		    continue
		if not self.flipped[x+a][y+b] and unflippedNeighborCount != flagCount:
		    self.beliefs[x+a][y+b] *= 1.0 - ((self.grid[x][y] - flagCount) / (float(unflippedNeighborCount) - flagCount))
		    print self.grid[x][y], (x+a, y+b), flagCount
		    if not self.flags[x+a][y+b] and self.beliefs[x+a][y+b] > 0:
		        self.antibeliefs[x+a][y+b] *= ((self.grid[x][y] - flagCount) / (float(unflippedNeighborCount) - flagCount))

        unflippedTiles = self.unflippedTiles()
        for i in range(self.height):
	    for j in range(self.width):
	        if not self.flipped[i][j] and (i, j) not in neighbors:
		    self.beliefs[i][j] *= 1.0 - (float(self.numMines - self.grid[x][y]) / (unflippedTiles - unflippedNeighborCount))
		    if not self.flags[i][j] and self.beliefs[i][j] > 0:
		        self.antibeliefs[i][j] *= (float(self.numMines - self.grid[x][y]) / (unflippedTiles - unflippedNeighborCount))

	for i in range(self.height):
	    for j in range(self.width):
	        if not self.flipped[i][j] and self.beliefs[i][j] == 0:
		    newFlagCount += 1
		    self.flags[i][j] = True

	return newFlagCount > allFlagCount

    def updateBeliefs(self):
	self.beliefs = [[1 - float(self.numMines)/(self.width*self.height) for i in range(self.width)] for j in range(self.height)]
	self.antibeliefs = [[float(self.numMines)/(self.width*self.height) for i in range(self.width)] for j in range(self.height)]
	newFlags = True
	while newFlags:
	    newFlags = False
            for i in range(self.height):
   	        for j in range(self.width):
	            if self.flipped[i][j]:
		        self.beliefs[i][j] = 0
		        self.antibeliefs[i][j] = 1
		        if self.grid[i][j] > 0:
		            newFlags = newFlags or self.actOnNeighbors(i, j)
			    if newFlags:
			        print newFlags

    def normalizeBeliefs(self):
        sumBeliefs = 0
        sumAntiBeliefs = 0
	unflippedTiles = self.unflippedTiles()

        maxBeliefs = 0
	maxAntiBeliefs = 0
        for i in range(self.height):
	    for j in range(self.width):
	        if not self.flipped[i][j]:
	            maxBeliefs = max(maxBeliefs, self.beliefs[i][j])
		    sumBeliefs += self.beliefs[i][j]
		    if not self.flags[i][j]:
		        sumAntiBeliefs += self.antibeliefs[i][j]
	                maxAntiBeliefs = max(maxAntiBeliefs, self.antibeliefs[i][j])

	for i in range(self.height):
	    for j in range(self.width):
	        #self.beliefs[i][j] *= (unflippedTiles - self.numMines) / sumBeliefs
		if not self.flipped[i][j]:
		    if sumBeliefs > 0:
		        self.beliefs[i][j] /= maxBeliefs
		    if sumAntiBeliefs > 0:
		        self.antibeliefs[i][j] /= maxAntiBeliefs

    def actOnBeliefs(self):
        maxval = 0
	argmax = (0, 0)

	for i in range(self.height):
	    for j in range(self.width):
	        belief = 1.0 - self.antibeliefs[i][j]
	        if belief >= maxval and not self.flags[i][j] and not self.flipped[i][j]:
		    maxval = belief
		    argmax = (i, j)

	self.flip(argmax[0], argmax[1])
	return self.grid[argmax[0]][argmax[1]] == -2

    def loss(self):
        for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j] and self.grid[i][j] == -2:
		    return True
        return False

    def finished(self):
        sumBeliefs = sum(sum(self.beliefs, []))
        return sumBeliefs == 0 or self.loss()

def main():  
    ms = minesweeper(8, 8, 10)
    gui = minesweeperGui(800, 800, ms)
    while True:
    #ms.grid = [[-2, 0, -2], [1, 2, 1], [0,0,0]]
    #ms.flipped = [[False, False, False], [True, True, True], [True,True,True]]
    #ms.beliefs = [[1.0/3, 1.0/3, 1.0/3], [0, 0, 0], [0,0,0]]

        while not ms.finished():
            gui.draw(ms)
            gui.window.update()
	    if ms.actOnBeliefs():
	        break
            ms.updateBeliefs()
	    ms.normalizeBeliefs()
	    time.sleep(3)

        gui.draw(ms)

        
        if ms.loss():
	    gui.lossScreen(ms)
        gui.window.update()

	raw_input("Press enter to continue")

        ms = minesweeper(8, 8, 10)

if __name__ == "__main__": main()
    

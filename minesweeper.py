from tkinter import *
import ImageTk
from PIL import Image
import random
import Queue
import time
import copy
import collections
import operator

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(operator.mul, xrange(n, n-r, -1), 1)
    denom = reduce(operator.mul, xrange(1, r+1), 1)
    return numer//denom

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
		    elif ms.grid[i][j] == -1 and False:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
	            else:
     		        self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.opened[ms.grid[i][j]])
		elif ms.beliefs[i][j] == 0 and False:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.flag)
		elif displayBeliefs:
  		    self.canvas.create_image(j*self.tileSize+self.offsx, i*self.tileSize+self.offsy, image=self.beliefs[int((ms.beliefs[i][j])*19)])
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

class Sampler():
    def __init__(self, grid, flipped, numMines):
        self.grid = copy.deepcopy(grid)
	self.width = len(grid[0])
	self.height = len(grid)
	self.flipped = copy.deepcopy(flipped)
	self.valid = True
	self.mines = [[False for i in range(self.width)] for j in range(self.height)]
	self.tileCount = 0

	for i in range(numMines-1):
	    pos = (random.randrange(self.height), random.randrange(self.width))
	    while self.mines[pos[0]][pos[1]] == True:
	        pos = (random.randrange(self.height), random.randrange(self.width))
	    self.mines[pos[0]][pos[1]] = True

	self.sparePos = (random.randrange(self.height), random.randrange(self.width))
	while self.mines[self.sparePos[0]][self.sparePos[1]] == True:
	    self.sparePos = (random.randrange(self.height), random.randrange(self.width))
	
	for i in range(self.height):
	    for j in range(self.width):
	        if self.mines[i][j]:
	            if self.flipped[i][j]:
			self.valid = False
			continue
	            for a in range(-1, 2):
	                for b in range(-1, 2):
		            if i+a < 0 or i+a >= self.height or j+b < 0 or j+b >= self.width:
		                continue
                            if self.flipped[i+a][j+b]:
		                self.grid[i+a][j+b] -= 1

        for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j]:
		    if self.grid[i][j] < 0:
		        self.valid = False
		    if self.grid[i][j] > 0:
		        self.tileCount += self.grid[i][j]


    def sample(self, pos):
        tileCount = self.tileCount

	if self.flipped[pos[0]][pos[1]]:
	    return False

        if self.valid:

	    if self.mines[pos[0]][pos[1]]:
	        pos = self.sparePos
 
            i, j = pos
            for a in range(-1, 2):
	        for b in range(-1, 2):
		    if i+a < 0 or i+a >= self.height or j+b < 0 or j+b >= self.width:
		        continue
		    if self.flipped[i+a][j+b]:
		        if self.grid[i+a][j+b]-1 < 0:
			    return False
		        tileCount -= 1
		    #if self.flipped[i+a][j+b]:
		    #    grid[i+a][j+b] -= 1
		    
        '''for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j] and grid[i][j] != 0:
		    return False'''

	return self.valid and tileCount == 0


class minesweeper():
    def __init__(self, w, h, numMines):
        self.grid = [[0 for i in range(w)] for j in range(h)]
	self.flipped = [[False for i in range(w)] for j in range(h)]
	self.beliefs = [[1 for i in range(w)] for j in range(h)]
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

    def sampleEvidenceGivenMineAtPos(self, pos, withNeighbors, numMines):
	if len(withNeighbors) == 0:
	    return True
        if self.flipped[pos[0]][pos[1]] or numMines+1 > len(withNeighbors):
	    return False
        mines = [[False for j in range(self.width)] for i in range(self.height)]
	mines[pos[0]][pos[1]] = True
	random.shuffle(withNeighbors)
	for i in range(numMines-1):
	    mines[withNeighbors[i][0]][withNeighbors[i][1]] = True
	if mines[pos[0]][pos[1]] == True:
	    mines[withNeighbors[numMines-1][0]][withNeighbors[numMines-1][1]] = True
	mines[pos[0]][pos[1]] = True
	
	copyGrid = copy.deepcopy(self.grid)
	copyGridSum = 0

	for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j]:
		    copyGridSum += copyGrid[i][j]
	        if mines[i][j]:
	            if self.flipped[i][j]:
	                return False
			#continue
	            for a in range(-1, 2):
	                for b in range(-1, 2):
		            if i+a < 0 or i+a >= self.height or j+b < 0 or j+b >= self.width:
		                continue
                            if self.flipped[i+a][j+b]:
		                copyGrid[i+a][j+b] -= 1
		    	        #if copyGrid[i+a][j+b] < 0:
			        #    return False

        sampleSum = 0
        for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j] and copyGrid[i][j] != 0:
		    return False
		    sampleSum += pow(copyGrid[i][j], 2)
		    copyGridSum += pow(8, 2)
        ret = 1 - (float(sampleSum)/max(copyGridSum, 1))
	return True

    def getListOfUnflippedTilesWithFlippedNeighbors(self):
        ret = []
	for i in range(self.height):
	    for j in range(self.width):
	        if self.flipped[i][j]:
		    continue
		for a in range(-1, 2):
		    for b in range(-1, 2):
		        if i+a < 0 or i+a >= self.height or j+b < 0 or j+b >= self.height:
			    continue
		        if self.flipped[i+a][j+b] and (i, j) not in ret:
			    ret.append((i, j))

	return ret 

    def sampleFromListOfProbs(self, probs):
        rand = random.random()
	runningTot = 0
	idx = 0

	while(runningTot < rand):
	    runningTot += probs[idx]
	    idx += 1
	
	return idx-1

    def getDistrOfPossibleMineCountsInNeighborRegion(self, withNeighbors):
        distr = [0 for i in range(self.numMines+1)]
	numSamples = 1000
	#iterate over all possible number of mines within evidence range
	for x in range(min(self.numMines+1, len(withNeighbors)+1)):
	    #take numSamples samples
	    for y in range(numSamples):
	        random.shuffle(withNeighbors)
                mines = [[False for j in range(self.width)] for i in range(self.height)]
		#randomly scatter x mines on grid within evidence range
	        for z in range(x):
		    mines[withNeighbors[z][0]][withNeighbors[z][1]] = True

                copyGrid = copy.deepcopy(self.grid)

		for i in range(self.height):
		    for j in range(self.width):
		        if mines[i][j]:
			    for a in range(-1, 2):
			        for b in range(-1, 2):
				    if i+a < 0 or i+a >= self.height or j+b < 0 or j+b >= self.width:
				        continue
				    if self.flipped[i+a][j+b]:
				        copyGrid[i+a][j+b] -= 1

		agreedWithEvidence = True
		for i in range(self.height):
		    for j in range(self.width):
		        if self.flipped[i][j] and copyGrid[i][j] != 0:
			    agreedWithEvidence = False

	        distr[x] += agreedWithEvidence

        sumElems = sum(distr)
	for i in range(len(distr)):
	    distr[i] /= float(max(sumElems, 1))

	return distr

    def updateBeliefs(self):
        '''
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
			        print newFlags'''

        '''
	withNeighbors = self.getListOfUnflippedTilesWithFlippedNeighbors()
	distrList = self.getDistrOfPossibleMineCountsInNeighborRegion(withNeighbors)
	print distrList
	print self.sampleFromListOfProbs(distrList)
        flippedTiles = self.height * self.width - self.unflippedTiles()

	for i in range(self.height):
	    for j in range(self.width):
	        sampleCount = 0
		posSampleCount = 0
		numSamples = max(ncr(len(withNeighbors), self.sampleFromListOfProbs(distrList)) * 100, 10)
	        for a in range(numSamples):
		    sampleCount += 1
	            numMines = self.sampleFromListOfProbs(distrList)
		    posSampleCount += float(self.sampleEvidenceGivenMineAtPos((i, j), withNeighbors, numMines))
		if (i, j) in withNeighbors:
		    posSampleCount *= (1-float(ncr(len(withNeighbors), numMines)) / ncr(self.height * self.width, numMines))
		else:
		    posSampleCount *= (1-float(ncr(self.height * self.width - len(withNeighbors), numMines)) / ncr(self.height * self.width, numMines))
		print float(ncr(len(withNeighbors), numMines)) / ncr(self.height * self.width, numMines)
		self.beliefs[i][j] = float(posSampleCount)/(sampleCount)
		print self.beliefs[i][j]'''
	
	self.beliefs = [[0 for i in range(self.width)] for j in range(self.height)]

        numSamples = 10000
	for a in range(numSamples):
	    sampler = Sampler(self.grid, self.flipped, self.numMines)
	    for i in range(self.height):
	        for j in range(self.width):
		    self.beliefs[i][j] += sampler.sample((i, j))



	

    def normalizeBeliefs(self):
        sumBeliefs = 0
        sumAntiBeliefs = 0
	unflippedTiles = self.unflippedTiles()

        maxBeliefs = 0
	minBeliefs = 999999
	maxAntiBeliefs = 0
        for i in range(self.height):
	    for j in range(self.width):
	        if not self.flipped[i][j]:
	            maxBeliefs = max(maxBeliefs, self.beliefs[i][j])
		    minBeliefs = min(minBeliefs, self.beliefs[i][j])
		    sumBeliefs += self.beliefs[i][j]
		    if not self.flags[i][j]:
		        sumAntiBeliefs += self.antibeliefs[i][j]
	                maxAntiBeliefs = max(maxAntiBeliefs, self.antibeliefs[i][j])

	for i in range(self.height):
	    for j in range(self.width):
	        #self.beliefs[i][j] *= (unflippedTiles - self.numMines) / sumBeliefs
		if not self.flipped[i][j]:
		    if sumBeliefs > 0:
		        self.beliefs[i][j] = (float(self.beliefs[i][j])) /  max((maxBeliefs), 1)
		    if sumAntiBeliefs > 0:
		        self.antibeliefs[i][j] /= maxAntiBeliefs

	print self.beliefs
	print self.flipped


    def actOnBeliefs(self):
        maxval = float('inf')
	argmax = (0, 0)

	for i in range(self.height):
	    for j in range(self.width):
	        belief = self.beliefs[i][j]
	        if belief <= maxval and not self.flipped[i][j]:
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
    w = 3
    h = 3
    n = 2
    ms = minesweeper(w, h, n)
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
	    time.sleep(0)

        gui.draw(ms)

        
        if ms.loss():
	    gui.lossScreen(ms)
        gui.window.update()

	raw_input("Press enter to continue")

        ms = minesweeper(w, h, n)

if __name__ == "__main__": main()
    

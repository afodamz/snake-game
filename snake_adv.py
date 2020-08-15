"""Snake Game """

import pygame
import tkinter as tk
import math
import random
from tkinter import messagebox
import os

class cube(object):
	rows = 20
	w = 500
	def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)


	def draw(self, surface, eyes=False):
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
		if eyes:
			centre = dis//2
			radius = 3
			circlemiddle = (i*dis+centre-radius, j*dis+8)
			circlemiddle2 = (i*dis + dis - radius*2, j*dis+8)
			pygame.draw.circle(surface, (0,0,0), circlemiddle, radius)
			pygame.draw.circle(surface, (0,0,0), circlemiddle2, radius)




class snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1

	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()
			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					if keys[pygame.K_RIGHT]:
						self.dirnx = -1
						self.dirny = 0
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					if keys[pygame.K_LEFT]:
						self.dirnx = 1
						self.dirny = 0
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


				elif keys[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					if keys[pygame.K_DOWN]:
						self.dirnx = 0
						self.dirny = -1
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


				elif keys[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					if keys[pygame.K_UP]:
						self.dirnx = 0
						self.dirny = 1
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


		# we are gonna get the index, cube object of the snake
		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)

			else:
				if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
				else: c.move(c.dirnx, c.dirny)


	def reset(self, pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def addcube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx==1 and dy==0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx==0 and dy==1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx==0 and dy==-1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy


	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)


def drawGrid(w, rows, surface):
	sizeBtwn = w // rows

	x = 0
	y = 0
	for i in range(rows):
		x = x + sizeBtwn
		y = y + sizeBtwn
		# draw the grid lines(surface, color, length)
		pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
		pygame.draw.line(surface, (255,255,255), (0,y),(w,y))




def game_sound(file):
	music_path = os.path.join("sounds", file)
	pygame.init()
	pygame.mixer.music.load(path)
	pygame.mixer.play(-1)

def play_sound(file):
	music_path = os.path.join("sounds", file)
	pygame.init()
	sound = pygame.mixer.Sound(os.path.join("sounds", 'eat.wav'))
	sound.play()


def redrawWindow(surface):
	global rows, width, color, s, food, score, myFont, scores
	surface.fill((11, 238, 207))
	s.draw(surface)
	food.draw(surface)
	drawGrid(width, rows, surface)
	draw_score(width, height, surface, myFont, score)
	pygame.display.update()

def randomFood(rows, item):
	positions = item.body

	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)

		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			continue
		else:
			break
	return (x,y)


def message_box(subject, content):
	# to make sure the tkinter messagebox comesup ontop
    global run
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    iExit = messagebox.askyesno(subject, content)
    if iExit > 0:
        try:
            root.destroy()
        except:
            pass
        return
    else:
        root.destroy()
        run = False
        return
	# messagebox.showinfo(subject, content)
    #
	# try:
	# 	root.destroy()
	# except:
	# 	pass

def draw_score(width, height, surface, Font, score):
	text = "SCORE: " + str(score)
	label = Font.render(text, 1, (255,255,0))
	surface.blit(label, (width - 250, height - 30))


def check_high_score():
	global score, scores
	for old_score in scores:
		if score > max(scores):
			scores.append(score)
			if len(scores) > 6:
				scores.pop()
			result = ("Snake master", str(score))
			scores.reverse()
			print(scores)
			return str(result)
		elif score > old_score:
			scores.append(score)
			if len(scores) > 6:
				scores.pop()
			result =("High Score", str(score))
			scores.reverse()
			print(scores)
			return str(result)
		else:
			result = ("Score", str(score))
			scores.reverse()
			print(scores)
			return str(result)
	return str(result)



def main():
	global width, height, rows, color, s, food, myFont, score, run, scores
	pygame.init()
	width = 500
	height = 500
	rows = 20
	score = 0
	scores = [0]
	scores.reverse()
	window = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Python snake xendia")

	# snake color and position
	s = snake((255, 0, 0), (10, 10))
	myFont = pygame.font.SysFont("monospace", 25, bold=10)
	food = cube(randomFood(rows, s), color=(0,255,0))

	run = True
	#This is to make sure that the game doesnt run at 10blocks persec
	clock = pygame.time.Clock()

	while run:
		pygame.time.delay(50) #pygame delay for 5 milliseonds

		clock.tick(10)
		s.move()

		if s.body[0].pos == food.pos:
			s.addcube()
			food = cube(randomFood(rows, s), color=(0,255,0))
			play_sound('eat.wav')
			score += 10


		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
				# play_sound('game_over.mp3')
				scores.append(score)
				scores.reverse()
				message_box("you lost", (check_high_score() + "\n play again?"))
				score = 0
				s.reset((10,10))
				break

		redrawWindow(window)




if __name__ == '__main__':

	# cube.rows = rows
	# cube.w  = w

	main()
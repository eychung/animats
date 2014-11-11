import math
import pygame
from pygame.locals import *
from resources import Resources 

class Beaver(pygame.sprite.Sprite):
	"""A beaver that will move across the screen
	Returns: beaver object
	Functions: update, calcnewpos
	Attributes: area, vector"""

	def __init__(self, vector):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = Resources.load_png('beaver.png')
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.vector = vector

	def update(self):
		newpos = self.calcnewpos(self.rect, self.vector)
		self.rect = newpos

	def calcnewpos(self, rect, vector):
		(angle, z) = vector
		(dx, dy) = (z*math.cos(angle), z*math.sin(angle))
		return rect.move(dx, dy)

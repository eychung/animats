import math
import pygame
from pygame.locals import *
from resources import Resources 

class Beaver(pygame.sprite.Sprite):
	"""A beaver that will move across the screen
	Returns: beaver object
	Functions: update, calcnewpos
	Attributes: energy, rect, vector"""

	def __init__(self, vector):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = Resources.load_png('beaver.png')
		originalsize = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (int(originalsize[0]/2), int(originalsize[1]/2)))
		screen = pygame.display.get_surface()
		self.rect = self.image.get_rect()

		self.energy = 100
		self.vector = vector

	def updateenergy(self):
		pass

	def update(self):
		newpos = self.calcnewpos(self.rect, self.vector)
		self.rect = newpos

	def calcnewpos(self, rect, vector):
		(angle, z) = vector
		(dx, dy) = (z*math.cos(angle), z*math.sin(angle))
		return rect.move(dx, dy)

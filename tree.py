import math
import pygame
import random
from pygame.locals import *
from resources import Resources 

class Tree(pygame.sprite.Sprite):
	"""A tree that
	Returns: tree object
	Functions: update, calcnewpos
	Attributes: vector"""

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = Resources.load_png('tree.png')
		screen = pygame.display.get_surface()
		self.rect.move_ip(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
		self.area = screen.get_rect()

	def update(self):
		pass

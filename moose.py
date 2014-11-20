import pygame
from pygame.locals import *
from resources import Resources

class Moose(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('moose.png')
    self.rect = self.image.get_rect()

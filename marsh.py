import math
import pygame
import random
from pygame.locals import *
from resources import Resources

class Marsh(pygame.sprite.Sprite):
  """A marsh
  Returns: marsh object
  Functions: update"""

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('marsh.png')

    # Scales and centers marsh
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0] / 2), int(originalsize[1] / 2)))
    newsize = self.image.get_size()
    screen = pygame.display.get_surface()
    centerx = screen.get_width() / 2 - newsize[0] / 2
    centery = screen.get_height() / 2 - newsize[1] / 2
    self.rect = self.image.get_rect()
    self.rect.move_ip(centerx, centery)

    self.scale = 1

  def update(self):
    pass

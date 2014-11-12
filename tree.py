import math
import pygame
import random
from pygame.locals import *
from resources import Resources

class Tree(pygame.sprite.Sprite):
  """A tree
  Returns: tree object
  Functions: update
  Attributes: health"""

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('tree.png')
    self.health = 100

    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0] / 2), int(originalsize[1] / 2)))
    self.rect = self.image.get_rect()

    # Tweak to avoid clipped images by right and bottom borders
    screen = pygame.display.get_surface()
    newsize = self.image.get_size()
    newposx = random.randint(0, screen.get_width() - newsize[0])
    newposy = random.randint(0, screen.get_height() - newsize[1])
    self.rect.move_ip(newposx, newposy)

  def update(self):
    pass

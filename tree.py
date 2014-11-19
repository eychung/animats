import math
import pygame
import random
from pygame.locals import *
from resources import Resources

class Tree(pygame.sprite.Sprite):
  """A tree
  Returns: tree object
  Functions: update
  Attributes: health, healthbar, state
  """

  CONST_STATE_IDLE = 0
  CONST_STATE_ATE = 1
  CONST_STATE_FORAGED = 2

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('tree.png')

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

    self.health = 100
    self.healthbar = self.rect.width
    self.state = self.CONST_STATE_IDLE

  def setstate(self, state):
    self.state = state

  def updatehealth(self):
    if self.state == self.CONST_STATE_ATE:
      self.health -= 1
    elif self.state == self.CONST_STATE_FORAGED:
      self.health -= 50
    self.healthbar = self.rect.width * min(1, (self.health/100.0))

  def update(self):
    self.updatehealth()


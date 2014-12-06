import math
import pygame
import random
from pygame.locals import *
from resources import Resources
from constants import Constants
from parameters import TreeParameters

INITIAL_HEALTH = TreeParameters.INITIAL_HEALTH
HEALTH_EATEN_COST = TreeParameters.HEALTH_EATEN_COST
HEALTH_FORAGED_COST = TreeParameters.HEALTH_FORAGED_COST

class Tree(pygame.sprite.Sprite):
  """A tree
  Returns: tree object
  Functions: update
  Attributes: health, healthbar, state
  """

  def __init__(self):
    self.respawn()

  def respawn(self):
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

    self.health = INITIAL_HEALTH
    self.healthbar = self.rect.width
    self.state = Constants.TREE_STATE_IDLE

  def setstate(self, state):
    self.state = state

  def updatehealth(self):
    if self.state == Constants.TREE_STATE_ATE:
      self.health -= HEALTH_EATEN_COST
    elif self.state == Constants.TREE_STATE_FORAGED:
      self.health -= HEALTH_FORAGED_COST
    self.healthbar = self.rect.width * min(1, (self.health/100.0))

  def update(self):
    self.updatehealth()


import math
import pygame
import random
from pygame.locals import *
from constants import Constants
from resources import Resources
from parameters import MarshParameters

INITIAL_HEALTH = MarshParameters.INITIAL_HEALTH
MAX_HEALTH = MarshParameters.MAX_HEALTH
MIN_HEALTH = MarshParameters.MIN_HEALTH

LOW_HEALTH_THRESHOLD = MarshParameters.LOW_HEALTH_THRESHOLD
MED_HEALTH_THRESHOLD = MarshParameters.MED_HEALTH_THRESHOLD

HEALTH_LUMBER_GAIN = MarshParameters.HEALTH_LUMBER_GAIN
HEALTH_IDLE_COST = MarshParameters.HEALTH_IDLE_COST

class Marsh(pygame.sprite.Sprite):
  """A marsh
  Returns: marsh object
  Functions: update
  Attributes: health, healthbar, scale
  """

  def __init__(self):
    self.health = INITIAL_HEALTH

    self.updatemodcounter = 0
    self.redraw()

    self.healthbar = self.rect.width * min(1, (self.health/100.0))

  def redraw(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('marsh.png')

    originalsize = self.image.get_size()
    self.fullsize = (int(originalsize[0]/2), int(originalsize[1]/2))

    # scale image according to health
    self.image = pygame.transform.scale(
      self.image, (int((self.health/100.0) * self.fullsize[0]),
                   int((self.health/100.0) * self.fullsize[1])))
    newsize = self.image.get_size()
    screen = pygame.display.get_surface()
    centerx = screen.get_width()/2 - newsize[0]/2
    centery = screen.get_height()/2 - newsize[1]/2
    self.rect = self.image.get_rect()
    self.rect.move_ip(centerx, centery)

  def gethealth(self):
    return self.health

  def gethealthlevel(self):
    if self.health < LOW_HEALTH_THRESHOLD:
      return Constants.BEAVER_STATE_MARSH_HEALTH_LOW
    elif self.health < MED_HEALTH_THRESHOLD:
      return Constants.BEAVER_STATE_MARSH_HEALTH_MED
    else:
      return Constants.BEAVER_STATE_MARSH_HEALTH_HIGH

  def improve(self):
    self.health += HEALTH_LUMBER_GAIN

    if self.health > MAX_HEALTH:
      self.health = MAX_HEALTH

    self.healthbar = self.rect.width * min(1, (self.health/100.0))

  def updatehealth(self):
    self.health -= HEALTH_IDLE_COST

    # marsh cannot die
    if self.health < MIN_HEALTH:
      self.health = MIN_HEALTH

    self.healthbar = self.rect.width * min(1, (self.health/100.0))

  def update(self):
    self.updatehealth()
    self.redraw()

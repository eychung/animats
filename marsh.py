import math
import pygame
import random
from pygame.locals import *
from resources import Resources

MIN_HEALTH = 10

class Marsh(pygame.sprite.Sprite):
  """A marsh
  Returns: marsh object
  Functions: update
  Attributes: health, healthbar, scale
  """

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('marsh.png')

    # Scales and centers marsh
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0]/2), int(originalsize[1]/2)))
    newsize = self.image.get_size()
    screen = pygame.display.get_surface()
    centerx = screen.get_width()/2 - newsize[0]/2
    centery = screen.get_height()/2 - newsize[1]/2
    self.rect = self.image.get_rect()
    self.rect.move_ip(centerx, centery)

    self.health = 100
    self.healthbar = self.rect.width / 2
    self.fullsize = newsize
    self.scale = 1
    self.updatemodcounter = 0

  def updatehealth(self):
    self.health -= 0.025
    self.healthbar = self.rect.width * min(1, (self.health/100.0))

    # reset marsh when health too low
    if self.health <= MIN_HEALTH:
      self = self.__init__()

  def updateimagesize(self):
    # only update the image every X steps, makes the image scale cleaner
    imageupdate = self.updatemodcounter % 100
    if imageupdate == 0:
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
    self.updatemodcounter = imageupdate + 1

  def update(self):
    self.updatehealth()
    self.updateimagesize()
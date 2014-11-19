import math
import pygame
from pygame.locals import *
from operator import itemgetter
from resources import Resources

class Beaver(pygame.sprite.Sprite):
  """A beaver that will move across the screen
  Returns: beaver object
  Functions: update, calcnewpos
  Attributes: energy, energybar, rect, vector
  """

  CONST_VIEW_DIST = 100

  def __init__(self, vector):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('beaver.png')
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0]/2), int(originalsize[1]/2)))
    self.rect = self.image.get_rect()

    self.energy = 100
    self.energybar = self.rect.width
    self.eyeview = []
    self.vector = vector

  """The beaver can observe trees within a 100x100 rect.
  Saves trees within eye viewing distance into internal list.
  """
  def seteyeview(self, treelist):
    x = self.rect.centerx - self.CONST_VIEW_DIST
    y = self.rect.centery - self.CONST_VIEW_DIST
    eyeviewrect = Rect(x, y, self.CONST_VIEW_DIST*2, self.CONST_VIEW_DIST*2)
    self.eyeview = []
    for tree in treelist:
      if eyeviewrect.colliderect(tree.rect):
        self.eyeview.append((tree, 
          self.calcrectcenterdistance(self.rect, tree.rect)))
        print self.rect.center
        print tree.rect.center

  def setscentview(self, animatslist):
    pass

  def calcrectcenterdistance(self, r1, r2):
    return math.hypot(r2.centerx - r1.centerx, r2.centery - r1.centery)

  """Values of the eight adjacent spots the beaver can move to.
  In the future, we may influence these values based on proximity
  to home as well or simply have it learn it.
  """
  def calcadjvals(self):
    sortedeyeview = sorted(self.eyeview, key=itemgetter(1))
    print sortedeyeview

  def calcnewpos(self, rect, vector):
    (angle, z) = vector
    (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
    return rect.move(dx, dy)

  def updateenergy(self):
    self.energybar = self.rect.width * (self.energy/100)

  def update(self):
    self.energy -= .05
    self.updateenergy()
    newpos = self.calcnewpos(self.rect, self.vector)
    self.rect = newpos

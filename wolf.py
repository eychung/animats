import math
import pygame
import random
from pygame.locals import *
from resources import Resources

class Wolf(pygame.sprite.Sprite):
  """A wolf that preys on beavers
  Attributes: adjpoints, rect, scentview, stepsize
  """

  CONST_SCENT_DIST = 200
  CONST_STEP_SIZE = 2

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('wolf.png')
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0]/2), int(originalsize[1]/2)))
    newsize = self.image.get_size()
    self.rect = self.image.get_rect()

    self.scentview = []
    self.stepsize = self.CONST_STEP_SIZE

    # Top left, top, top right, left, right, bottom left, bottom, bottom right
    self.setadjpoints()

    print self.adjpoints
    print self.rect

  def setadjpoints(self):
    self.adjpoints = [
      (self.rect.centerx - self.stepsize, # top left
      self.rect.centery - self.stepsize),
      (self.rect.centerx, # top
      self.rect.centery - self.stepsize),
      (self.rect.centerx + self.stepsize, # top right
      self.rect.centery - self.stepsize), 
      (self.rect.centerx - self.stepsize, # left
      self.rect.centery),
      (self.rect.centerx + self.stepsize, # right
      self.rect.centery),
      (self.rect.centerx - self.stepsize, # bottom left
      self.rect.centery + self.stepsize),
      (self.rect.centerx, # bottom
      self.rect.centery + self.stepsize),
      (self.rect.centerx + self.stepsize, # bottom right
      self.rect.centery + self.stepsize)]

  def setstepsize(self, stepsize):
    self.stepsize = stepsize

  def setscentview(self, beaver):
    x = self.rect.centerx - self.CONST_SCENT_DIST
    y = self.rect.centery - self.CONST_SCENT_DIST
    scentviewrect = Rect(x, y, self.CONST_SCENT_DIST*2, self.CONST_SCENT_DIST*2)
    self.scentview = []
    if scentviewrect.colliderect(beaver.rect):
      self.scentview.append(beaver)

  def calcadjvals(self):
    adjvals = []
    if self.scentview:
      print self.adjpoints
      for point in self.adjpoints:
        shortestdist = Resources.calcdistance(point, self.scentview[0].rect.center)
        normalizeddist = shortestdist/(self.CONST_SCENT_DIST * math.sqrt(2))
        adjvals.append(1 - normalizeddist)
    return adjvals

  def calcnewpos(self, rect):
    self.setadjpoints()
    adjvals = self.calcadjvals()
    if adjvals:
      moveto = self.adjpoints[adjvals.index(max(adjvals))]
      offsetx = moveto[0] - self.rect.centerx
      offsety = moveto[1] - self.rect.centery
      print "moving to " + str(moveto)
      return rect.move(offsetx, offsety)
    else: # Move randomly
      offsetx = (random.randint(0, 1)*2 - 1) * self.stepsize
      offsety = (random.randint(0, 1)*2 - 1) * self.stepsize
      print "moving randomly" + str(offsetx) + " and " + str(offsety)
      return rect.move(offsetx, offsety)

  def update(self):
    newpos = self.calcnewpos(self.rect)
    self.rect = newpos


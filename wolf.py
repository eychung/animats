import math
import pygame
import random
from pygame.locals import *
from marsh import Marsh
from resources import Resources

class Wolf(pygame.sprite.Sprite):
  """A wolf that preys on beavers
  Attributes: adjpoints, eyeview, rect, scentview, stepsize
  """

  CONST_VIEW_DIST = 100
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

    self.eyeview = []
    self.scentview = []
    self.stepsize = self.CONST_STEP_SIZE

    # Top left, top, top right, left, right, bottom left, bottom, bottom right
    self.setadjpoints()

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

  def seteyeview(self, terrain):
    x = self.rect.centerx - self.CONST_VIEW_DIST
    y = self.rect.centery - self.CONST_VIEW_DIST
    eyeviewrect = Rect(x, y, self.CONST_VIEW_DIST*2, self.CONST_VIEW_DIST*2)
    self.eyeview = []
    for sprite in terrain:
      if isinstance(sprite, Marsh) and eyeviewrect.colliderect(sprite.rect):
        self.eyeview.append(sprite)

  def setscentview(self, beaver):
    x = self.rect.centerx - self.CONST_SCENT_DIST
    y = self.rect.centery - self.CONST_SCENT_DIST
    scentviewrect = Rect(x, y, self.CONST_SCENT_DIST*2, self.CONST_SCENT_DIST*2)
    self.scentview = []
    if scentviewrect.colliderect(beaver.rect):
      self.scentview.append(beaver)

  def calcadjvals(self):
    self.setadjpoints()
    adjvals = []
    if self.scentview:
      for point in self.adjpoints:
        shortestdist = Resources.calcdistance(point, self.scentview[0].rect.center)
        normalizeddist = shortestdist/(self.CONST_SCENT_DIST * math.sqrt(2))
        adjvals.append(1 - normalizeddist)
    return adjvals

  def calcnewpos(self, rect):
    adjvals = self.calcadjvals()
    if adjvals: # Beaver is present
      sortedadjvals = sorted(adjvals)
      while True:
        maxpoint = self.adjpoints[adjvals.index(max(adjvals))]
        # If wolf sees marsh, we must make sure it does not enter it
        if self.eyeview:
          newx = maxpoint[0] - self.rect.width/2
          newy = maxpoint[1] - self.rect.height/2
          temprect = pygame.Rect(newx, newy, self.rect.width, self.rect.height)
          # If maxpoint makes wolf go into marsh or off screen, we must find a new point
          if newx < 0 or newy < 0 or self.eyeview[0].rect.colliderect(temprect):
            adjvals[adjvals.index(max(adjvals))] = -403
          else:
            break
        # Wolf is not close to marsh, so move however
        else:
          break
      maxpoint = self.adjpoints[adjvals.index(max(adjvals))]
      offsetx = maxpoint[0] - self.rect.width/2 - self.rect.x
      offsety = maxpoint[1] - self.rect.height/2 - self.rect.y
      return rect.move(offsetx, offsety)
    else: # Move randomly
      offsetx = (random.randint(0, 1)*2 - 1) * self.stepsize
      offsety = (random.randint(0, 1)*2 - 1) * self.stepsize
      while True:
        offsetx = (random.randint(0, 1)*2 - 1) * self.stepsize
        offsety = (random.randint(0, 1)*2 - 1) * self.stepsize
        newx = self.rect.x + offsetx
        newy = self.rect.y + offsety
        # This assumes that the step size is greater than its view distance
        temprect = pygame.Rect(newx, newy, self.rect.width, self.rect.height)
        if newx >= 0 and newy >= 0:
          # If wolf does not see marsh, move however
          if not self.eyeview:
            break
          # If wolf sees marsh but next move will not move it into marsh
          elif self.eyeview and not self.eyeview[0].rect.colliderect(temprect):
            break
      return rect.move(offsetx, offsety)

  def update(self):
    newpos = self.calcnewpos(self.rect)
    self.rect = newpos


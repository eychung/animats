import math
import pygame
from pygame.locals import *
from operator import itemgetter
from resources import Resources

class Beaver(pygame.sprite.Sprite):
  """A beaver that will move across the screen
  Returns: beaver object
  Functions: update, calcnewpos
  Attributes: adjlist, energy, energybar, rect, vector
  """

  CONST_VIEW_DIST = 100
  CONST_STEP_SIZE = 1 # pixels

  def __init__(self, vector):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('beaver.png')
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0]/2), int(originalsize[1]/2)))
    self.rect = self.image.get_rect()

    # Top left, top, top right, left, right, bottom left, bottom, bottom right
    self.setadjpoints()
    self.energy = 100
    self.energybar = self.rect.width
    self.eyeview = []
    self.vector = vector

  def setadjpoints(self):
     self.adjpoints = [
      (self.rect.centerx - self.CONST_STEP_SIZE, # top left
      self.rect.centery - self.CONST_STEP_SIZE),
      (self.rect.centerx, # top
      self.rect.centery - self.CONST_STEP_SIZE),
      (self.rect.centerx + self.CONST_STEP_SIZE, # top right
      self.rect.centery - self.CONST_STEP_SIZE), 
      (self.rect.centerx - self.CONST_STEP_SIZE, # left
      self.rect.centery),
      (self.rect.centerx + self.CONST_STEP_SIZE, # right
      self.rect.centery),
      (self.rect.centerx - self.CONST_STEP_SIZE, # bottom left
      self.rect.centery + self.CONST_STEP_SIZE),
      (self.rect.centerx, # bottom
      self.rect.centery + self.CONST_STEP_SIZE),
      (self.rect.centerx + self.CONST_STEP_SIZE, # bottom right
      self.rect.centery + self.CONST_STEP_SIZE)]

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
        self.eyeview.append(tree)

  def setscentview(self, animatslist):
    pass

  def gettreedisttuple(self, treelist, point):
    treedisttuple = []
    for tree in treelist:
      treedisttuple.append((tree,
        self.calcdistance(point, tree.rect.center)))
    return treedisttuple

  def calcdistance(self, p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

  """Return a list of eight values for the beaver's adjacency list.
  High values are favored. In the future, we may either influence these
  values based on distance from home or learn it.

  """
  def calcadjvals(self):
    adjvals = []
    if self.eyeview:
      for point in self.adjpoints:
        treedisttuple = self.gettreedisttuple(self.eyeview, point)
        # Get the distance to the closest tree
        # Sorting may be useful for later ops
        shortestdist = sorted(treedisttuple, key=itemgetter(1))[0][1]
        normalizeddist = shortestdist/(self.CONST_VIEW_DIST * math.sqrt(2))
        adjvals.append(1 - normalizeddist)
    return adjvals

  def calcnewpos(self, rect):
    self.setadjpoints()
    adjvals = self.calcadjvals()
    moveto = self.adjpoints[adjvals.index(max(adjvals))]
    print str(self.rect.center) + " moving to " + str(moveto)
    # Note that the move function returns a new rect moved by offset
    offsetx = moveto[0] - self.rect.centerx
    offsety = moveto[1] - self.rect.centery
    return rect.move(offsetx, offsety)

  def updateenergy(self):
    self.energy -= .05
    self.energybar = self.rect.width * (self.energy/100)

  def update(self):
    self.updateenergy()
    newpos = self.calcnewpos(self.rect)
    self.rect = newpos

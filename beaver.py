import math
import pygame
import random
from pygame.locals import *
from operator import itemgetter
from resources import Resources

class Beaver(pygame.sprite.Sprite):
  """A beaver that will move across the screen
  Returns: beaver object
  Functions: update, calcnewpos
  Attributes: adjlist, energy, energybar, rect, state, vector
  """

  CONST_VIEW_DIST = 100
  CONST_STEP_SIZE = 1 # pixels

  CONST_STATE_WALK = 0
  CONST_STATE_EAT = 1
  CONST_STATE_FORAGE = 2

  def __init__(self, vector):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('beaver.png')
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0]/2), int(originalsize[1]/2)))
    newsize = self.image.get_size()
    self.rect = self.image.get_rect()

    # Centers the beaver to spawn in the center of the marshes
    screen = pygame.display.get_surface()
    centerx = screen.get_width()/2 - newsize[0]/2
    centery = screen.get_height()/2 - newsize[1]/2
    self.rect.move_ip(centerx, centery)

    # Top left, top, top right, left, right, bottom left, bottom, bottom right
    self.setadjpoints()
    self.energy = 100
    self.energybar = self.rect.width
    self.eyeview = []
    self.state = self.CONST_STATE_WALK
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

  def setstate(self, state):
      #print "beaver state is changed to " + str(state)
      self.state = state

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
    if self.state == self.CONST_STATE_WALK:
      self.setadjpoints()
      adjvals = self.calcadjvals()
      if adjvals:
        moveto = self.adjpoints[adjvals.index(max(adjvals))]
        print str(self.rect.center) + " moving to " + str(moveto)
        # Note that the move function returns a new rect moved by offset
        offsetx = moveto[0] - self.rect.centerx
        offsety = moveto[1] - self.rect.centery
        return rect.move(offsetx, offsety)
      else: # Pick random location to move to if can't view any nearby trees
        offsetx = random.randint(0, 1)*2 - 1 * self.CONST_STEP_SIZE
        offsety = random.randint(0, 1)*2 - 1 * self.CONST_STEP_SIZE
        return rect.move(offsetx, offsety)
    else: # CONST_STATE_EAT or CONST_STATE_FORAGE
      return self.rect # Don't move

  def updateenergy(self):
    if self.state == self.CONST_STATE_WALK:
      self.energy -= .05
    elif self.state == self.CONST_STATE_EAT:
      self.energy += .1
    elif self.state == self.CONST_STATE_FORAGE:
      self.energy -= .1
    self.energybar = self.rect.width * min(1, (self.energy/100.0))

  def update(self):
    # First check if need to change states
    if self.rect.collidelist(self.eyeview) >= 0:
      self.setstate(self.CONST_STATE_EAT)

    self.updateenergy()
    newpos = self.calcnewpos(self.rect)
    self.rect = newpos


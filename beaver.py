import math
import pygame
import random
from pygame.locals import *
from operator import itemgetter
from marsh import Marsh
from resources import Resources
from tree import Tree
from brain import Brain

class Beaver(pygame.sprite.Sprite):
  """A beaver that will move across the screen
  Returns: beaver object
  Functions: update, calcnewpos
  Attributes: adjlist, energy, energybar, eyeview, inwater, rect, scentview,
    state, stepsize
  """

  CONST_VIEW_DIST = 100
  CONST_SCENT_DIST = 200
  CONST_STEP_SIZE_LAND = 1 # pixels
  CONST_STEP_SIZE_WATER = 4

  CONST_STATE_WALK = 0
  CONST_STATE_EAT = 1
  CONST_STATE_FORAGE = 2

  def __init__(self):
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

    self.energy = 100
    self.energybar = self.rect.width
    self.eyeview = [] # Contains knowledge of nearby sprites by vision
    self.inwater = True # Beaver spawns in marsh
    self.scentview = [] # Contains knowledge of nearby wolf by scent
    self.state = self.CONST_STATE_WALK
    self.stepsize = self.CONST_STEP_SIZE_WATER

    # Top left, top, top right, left, right, bottom left, bottom, bottom right
    self.setadjpoints()

    self.brain = Brain()

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

  def setbrain(self, brain):
    self.brain = brain

  def setstate(self, state):
    #print "beaver state is changed to " + str(state)
    self.state = state

  def setstepsize(self, stepsize):
    self.stepsize = stepsize

  """The beaver can observe trees within a 100x100 rect.
  Saves trees within eye viewing distance into internal list.
  """
  def seteyeview(self, terrain):
    x = self.rect.centerx - self.CONST_VIEW_DIST
    y = self.rect.centery - self.CONST_VIEW_DIST
    eyeviewrect = Rect(x, y, self.CONST_VIEW_DIST*2, self.CONST_VIEW_DIST*2)
    self.eyeview = []
    for sprite in terrain:
      if eyeviewrect.colliderect(sprite.rect):
        self.eyeview.append(sprite)

  def setscentview(self, wolf):
    x = self.rect.centerx - self.CONST_SCENT_DIST
    y = self.rect.centery - self.CONST_SCENT_DIST
    scentviewrect = Rect(x, y, self.CONST_SCENT_DIST*2,
      self.CONST_SCENT_DIST*2)
    self.scentview = []
    if scentviewrect.colliderect(wolf.rect):
      self.scentview.append(wolf)

  def gettreedisttuple(self, spritelist, point):
    treedisttuple = []
    for sprite in spritelist:
      if isinstance(sprite, Tree):
        treedisttuple.append((sprite,
          Resources.calcdistance(point, sprite.rect.center)))
    return treedisttuple

  def gettreeview(self, view):
    treeinfo = []
    for sprite in view:
      if isinstance(sprite, Tree):
        treeinfo.append(sprite)
    return treeinfo

  """Return a list of eight values for the beaver's adjacency list.
  High values are favored. In the future, we may either influence these
  values based on distance from home or learn it.

  """
  def calcadjvalsfood(self):
    adjvals = []
    treeinfo = self.gettreeview(self.eyeview)
    if treeinfo:
      for point in self.adjpoints:
        treedisttuple = self.gettreedisttuple(treeinfo, point)
        # Get the distance to the closest tree
        # Sorting may be useful for later ops
        shortestdist = sorted(treedisttuple, key=itemgetter(1))[0][1]
        normalizeddist = shortestdist/(self.CONST_VIEW_DIST * math.sqrt(2) +
          math.sqrt(pow(treeinfo[0].rect.width, 2) + pow(treeinfo[0].rect.height, 2)))
        #normalizeddist = shortestdist/(self.CONST_VIEW_DIST * math.sqrt(2))
        adjvals.append(1 - normalizeddist)
    return adjvals

  def calcadjvalspred(self):
    adjvals = []
    if self.scentview:
      scentpoint = self.scentview[0].rect.center
      for point in self.adjpoints:
        scentdisttuple = [(self.scentview[0],
          Resources.calcdistance(scentpoint, point))]
        shortestdist = sorted(scentdisttuple, key=itemgetter(1))[0][1]
        normalizeddist = shortestdist/(self.CONST_VIEW_DIST * math.sqrt(2))
        adjvals.append(1 - normalizeddist)

    return adjvals

  def calcadjvalsmarsh(self):
    adjvals = []
    for sprite in self.eyeview:
      if isinstance(sprite, Marsh):
        marshpoint = sprite.rect.center
        for point in self.adjpoints:
          marshdisttuple = [(sprite,
            Resources.calcdistance(marshpoint, point))]
          shortestdist = sorted(marshdisttuple, key=itemgetter(1))[0][1]
          normalizeddist = shortestdist/(self.CONST_VIEW_DIST * math.sqrt(2))
          adjvals.append(1 - normalizeddist)
    return adjvals

  def calcnewpos(self, rect):
    if self.state == self.CONST_STATE_WALK:
      self.setadjpoints()
      adjvalsfood = self.calcadjvalsfood()
      adjvalspred = self.calcadjvalspred()
      adjvalsmarsh = self.calcadjvalsmarsh()
      adjpointidx = self.brain.getmaxadjidx(adjvalsfood, adjvalspred,
        adjvalsmarsh)

      if adjvalsfood:
        print "Using brain max in homing " + str(adjpointidx)
        #moveto = self.adjpoints[adjvalsfood.index(max(adjvalsfood))]
        moveto = self.adjpoints[adjpointidx]
        print "Fixed moving from " + str(self.rect.center) + " moving to " + str(moveto) + '\n'
        # Note that the move function returns a new rect moved by offset
        offsetx = moveto[0] - self.rect.width/2 - self.rect.x
        offsety = moveto[1] - self.rect.height/2 - self.rect.y
        return rect.move(offsetx, offsety)
      else: # Pick random location to move to if can't view any nearby trees
        print "Moving randomly and not using " + str(adjpointidx) + '\n'
        while True:
          offsetx = (random.randint(0, 1)*2 - 1) * self.stepsize
          offsety = (random.randint(0, 1)*2 - 1) * self.stepsize
          newx = self.rect.x + offsetx - self.rect.width/2
          newy = self.rect.y + offsety - self.rect.height/2
          if newx >= 0 and newy >= 0:
            break
        return rect.move(offsetx, offsety)
    else: # CONST_STATE_EAT or CONST_STATE_FORAGE
      return self.rect # Don't move

  def updateenergy(self):
    if self.state == self.CONST_STATE_WALK:
      if self.inwater:
        self.energy -= 0.025
      else:
        self.energy -= 0.5
    elif self.state == self.CONST_STATE_EAT:
      self.energy += .1
    elif self.state == self.CONST_STATE_FORAGE:
      self.energy -= .1
    self.energybar = self.rect.width * min(1, (self.energy/100.0))

  def updateloc(self):
    self.inwater = False
    for sprite in self.eyeview:
      if (isinstance(sprite, Marsh) and
        pygame.sprite.collide_rect(self, sprite)):
        self.inwater = True

  def update(self):
    # First, check if need to change states
    # If beaver is on tree, we assume it eats it
    if (self.gettreeview(self.eyeview) and
      self.rect.collidelist(self.gettreeview(self.eyeview)) >= 0):
      self.setstate(self.CONST_STATE_EAT)

    # Second, check if beaver is in water or not
    self.updateloc()
    if self.inwater:
      self.setstepsize(self.CONST_STEP_SIZE_WATER)
    else:
      self.setstepsize(self.CONST_STEP_SIZE_LAND)

    self.updateenergy()
    newpos = self.calcnewpos(self.rect)
    self.rect = newpos


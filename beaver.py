import math
import pygame
import random
from pygame.locals import *
from operator import itemgetter
from constants import Constants
from marsh import Marsh
from resources import Resources
from tree import Tree
from brain import Brain

class Beaver(pygame.sprite.Sprite):
  """A beaver that will move across the screen
  Returns: beaver object
  Functions: update, calcnewpos
  Attributes: action, adjlist, energy, energybar, eyeview, haslumber, inwater, rect,
    scentview, states, stepsize
  """

  CONST_VIEW_DIST = 100
  CONST_SCENT_DIST = 200
  CONST_STEP_SIZE_LAND = 1 # pixels
  CONST_STEP_SIZE_WATER = 4

  CONST_ACTION_WALK = 0
  CONST_ACTION_EAT = 1
  CONST_ACTION_FORAGE = 2

  CONST_LUMBER_WEIGHT = 2

  CONST_ENERGY_IDLE_COST = 0.1
  CONST_ENERGY_WALK_LAND_COST = 0.5
  CONST_ENERGY_WALK_WATER_COST = 0.25
  CONST_ENERGY_EAT_GAIN = 0.5
  CONST_ENERGY_PICK_UP_LUMBER_COST = 0.25
  # No cost in dropping lumber

  def __init__(self):
    self.reset()
    self.brain = Brain()

  def reset(self):
    # Centers the beaver to spawn in the center of the marshes
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Resources.load_png('beaver.png')
    originalsize = self.image.get_size()
    self.image = pygame.transform.scale(
      self.image, (int(originalsize[0]/2), int(originalsize[1]/2))) 
    self.rect = self.image.get_rect()
    newsize = self.image.get_size()
    screen = pygame.display.get_surface()
    centerx = screen.get_width()/2 - newsize[0]/2
    centery = screen.get_height()/2 - newsize[1]/2
    self.rect.move_ip(centerx, centery)

    self.action = self.CONST_ACTION_WALK
    self.energy = 100
    self.energybar = self.rect.width
    self.eyeview = [] # Contains knowledge of nearby sprites by vision
    self.haslumber = False
    self.inwater = True # Beaver spawns in marsh
    self.scentview = [] # Contains knowledge of nearby wolf by scent
    self.states = [Constants.BEAVER_STATE_BEAVER_ENERGY_HIGH,
      Constants.BEAVER_STATE_MARSH_HEALTH_LOW,
      Constants.BEAVER_STATE_NO_LUMBER,
      Constants.BEAVER_STATE_NONE_TREE,
      Constants.BEAVER_STATE_AT_MARSH,
      Constants.BEAVER_STATE_NONE_WOLF]
    self.stepsize = self.CONST_STEP_SIZE_WATER

    # Top left, top, top right, left, right, bottom left, bottom, bottom right
    self.setadjpoints()

  def respawn(self):
    self.reset()

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

  def setaction(self, action):
    #print "beaver action is changed to " + str(action)
    self.action = action

  def setstate(self, index, state):
    self.states[index] = state

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
      self.setstate(Constants.BEAVER_STATE_INDEX_WOLF,
        Constants.BEAVER_STATE_SEE_WOLF)
    else:
      self.setstate(Constants.BEAVER_STATE_INDEX_WOLF,
        Constants.BEAVER_STATE_NONE_WOLF)

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
          # TODO: May have to tweak this normalized distance
          normalizeddist = shortestdist/(self.CONST_VIEW_DIST * math.sqrt(2))
          adjvals.append(1 - normalizeddist)
    return adjvals

  # Obsolete method used for NN
  def calcnewpos(self, rect):
    if self.action == self.CONST_ACTION_WALK:
      self.setadjpoints()
      adjvalsfood = self.calcadjvalsfood()
      adjvalspred = self.calcadjvalspred()
      adjvalsmarsh = self.calcadjvalsmarsh()
      #adjpointidx = self.brain.getmaxadjidx(adjvalsfood, adjvalspred, adjvalsmarsh)

      if adjvalsfood:
        #print "Using brain max in homing " + str(adjpointidx)
        moveto = self.adjpoints[adjvalsfood.index(max(adjvalsfood))]
        #moveto = self.adjpoints[adjpointidx]
        print "Fixed moving from " + str(self.rect.center) + " moving to " + str(moveto) + '\n'
        # Note that the move function returns a new rect moved by offset
        offsetx = moveto[0] - self.rect.width/2 - self.rect.x
        offsety = moveto[1] - self.rect.height/2 - self.rect.y
        return rect.move(offsetx, offsety)
      else: # Pick random location to move to if can't view any nearby trees
        #print "Moving randomly and not using " + str(adjpointidx) + '\n'
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

  # Use this method only if knows there is a tree nearby and not at tree already
  # If violation of rules when method called, beaver doesn't move and still lose energy.
  def performactionmovetotree(self):
    self.setadjpoints()
    adjvalsfood = self.calcadjvalsfood()
    if (self.gettreeview(self.eyeview) and
      self.rect.collidelist(self.gettreeview(self.eyeview)) >= 0):
      print "performactionmovetotree: already at tree!"
      self.energy -= Beaver.CONST_ENERGY_IDLE_COST
      return self.rect
    elif adjvalsfood:
      moveto = self.adjpoints[adjvalsfood.index(max(adjvalsfood))]
      offsetx = moveto[0] - self.rect.width/2 - self.rect.x
      offsety = moveto[1] - self.rect.height/2 - self.rect.y
      if self.haslumber:
        if self.inwater:
          self.energy -= (Beaver.CONST_ENERGY_WALK_WATER_COST *
            Beaver.CONST_LUMBER_WEIGHT)
        else:
          self.energy -= (Beaver.CONST_ENERGY_WALK_LAND_COST *
            Beaver.CONST_LUMBER_WEIGHT)
      else:
        if self.inwater:
          self.energy -= Beaver.CONST_ENERGY_WALK_WATER_COST
        else:
          self.energy -= Beaver.CONST_ENERGY_WALK_LAND_COST
      return rect.move(offsetx, offsety)
    else:
      print "performactionmovetotree: no trees in sight - unable to move to nearest tree"
      self.energy -= Beaver.CONST_ENERGY_IDLE_COST
      return self.rect

  # Use this method only if knows there is a marsh nearby and not in marsh already
  # If violation of rules when method called, beaver doesn't move and still loses energy.
  def performactionmovetomarsh(self):
    self.setadjpoints()
    adjvalsmarsh = self.calcadjvalsmarsh()
    if self.inwater:
      print "performactionmovetomarsh: already on marsh!"
      self.energy -= Beaver.CONST_ENERGY_IDLE_COST
      return self.rect
    elif adjvalsmarsh:
      moveto = self.adjpoints[adjvalsmarsh.index(max(adjvalsmarsh))]
      offsetx = moveto[0] - self.rect.width/2 - self.rect.x
      offsety = moveto[1] - self.rect.height/2 - self.rect.y
      if self.haslumber:
        self.energy -= (Beaver.CONST_ENERGY_WALK_LAND_COST *
          Beaver.CONST_LUMBER_WEIGHT)
      else:
        self.energy -= Beaver.CONST_ENERGY_WALK_LAND_COST # Moving on land
      return rect.move(offsetx, offsety)
    else:
      print "performactionmovetomarsh: no marsh in sight - unable to move to marsh"
      self.energy -= Beaver.CONST_ENERGY_IDLE_COST
      return self.rect

  # Use this method only if beaver is at a tree
  def performactioneat(self):
    if (self.gettreeview(self.eyeview) and
      self.rect.collidelist(self.gettreeview(self.eyeview)) >= 0):
      self.energy += Beaver.CONST_ENERGY_EAT_GAIN
      return self.rect
    else:
      print "performactioneat: not at tree - cannot eat"
      self.energy -= Beaver.CONST_ENERGY_IDLE_COST
      return self.rect

  def performactionpickuplumber(self):
    if (self.gettreeview(self.eyeview) and
      self.rect.collidelist(self.gettreeview(self.eyeview)) >= 0):
      self.haslumber = True
      self.setstate(Constants.BEAVER_STATE_INDEX_LUMBER,
        Constants.BEAVER_STATE_HAS_LUMBER)
      self.energy -= Beaver.CONST_ENERGY_PICK_UP_LUMBER_COST
      return self.rect
    else:
      print "performactionpickuplumber: not at tree - cannot pick up lumber"
      return self.rect

  # Can drop lumber anywhere resulting in 0 energy change; doesn't have to be in marsh to drop it
  def performactiondroplumber(self):
    self.haslumber = False
    self.setstate(Constants.BEAVER_STATE_INDEX_LUMBER,
      Constants.BEAVER_STATE_NO_LUMBER)
    return self.rect

  def updateenergy(self):
    if self.energy == 0:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_ZERO)
    elif self.energy < 30:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_LOW)
    elif self.energy < 70:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_MED)
    else:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_HIGH)

  def updateenergynobrain(self):
    if self.action == self.CONST_ACTION_WALK:
      if self.inwater:
        self.energy -= Beaver.CONST_ENERGY_WALK_WATER_COST
      else:
        self.energy -= Beaver.CONST_ENERGY_WALK_LAND_COST
    elif self.action == self.CONST_ACTION_EAT:
      self.energy += Beaver.CONST_ENERGY_EAT_GAIN
    elif self.action == self.CONST_ACTION_FORAGE:
      self.energy -= Beaver.CONST_ENERGY_PICK_UP_LUMBER_COST

    # Set beaver energy state
    if self.energy == 0:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_ZERO)
    elif self.energy < 30:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_LOW)
    elif self.energy < 70:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_MED)
    else:
      self.setstate(Constants.BEAVER_STATE_INDEX_BEAVER_ENERGY,
        Constants.BEAVER_STATE_BEAVER_ENERGY_HIGH)

    self.energybar = self.rect.width * min(1, (self.energy/100.0))

  def updatetreeresponse(self):
    self.setstate(Constants.BEAVER_STATE_INDEX_TREE,
      Constants.BEAVER_STATE_NONE_TREE)
    if self.gettreeview(self.eyeview):
      self.setstate(Constants.BEAVER_STATE_INDEX_TREE,
        Constants.BEAVER_STATE_SEE_TREE)
      if self.rect.collidelist(self.gettreeview(self.eyeview)) >= 0:
        # If beaver is on tree, we assume it eats it for now
        self.setaction(self.CONST_ACTION_EAT)
        self.setstate(Constants.BEAVER_STATE_INDEX_TREE,
          Constants.BEAVER_STATE_AT_TREE)

  def updateterraintyperesponse(self):
    # If beaver does not see marsh, assume it retains previous knowledge of it
    self.inwater = False
    self.setstepsize(self.CONST_STEP_SIZE_LAND)
    self.setstate(Constants.BEAVER_STATE_INDEX_MARSH,
      Constants.BEAVER_STATE_NONE_MARSH)
    for sprite in self.eyeview:
      if isinstance(sprite, Marsh):
        self.setstate(Constants.BEAVER_STATE_INDEX_MARSH_HEALTH,
          sprite.gethealthlevel())
        self.setstate(Constants.BEAVER_STATE_INDEX_MARSH,
          Constants.BEAVER_STATE_SEE_MARSH)
        if pygame.sprite.collide_rect(self, sprite):
          self.inwater = True
          self.setstepsize(self.CONST_STEP_SIZE_WATER)
          self.setstate(Constants.BEAVER_STATE_INDEX_MARSH,
            Constants.BEAVER_STATE_AT_MARSH)

  def update(self):
    # First, update tree response
    self.updatetreeresponse()

    # Second, update terrain type response
    self.updateterraintyperesponse()
 
    # No brain movement
    newpos = self.calcnewpos(self.rect)
    self.rect = newpos
    self.updateenergynobrain()

    # Brain movement
    # perform action, then update energy

    self.brain.setstates(self.states)
    print self.states

# TODO: It is actually observed that beavers can eat trees while in marsh


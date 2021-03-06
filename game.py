import pygame
from pygame.locals import *
from beaver import Beaver
from brain import Brain
from constants import Constants
from parameters import GameParameters
from marsh import Marsh
from terrain import Terrain
from tree import Tree
from wolf import Wolf

BG_COLOR = GameParameters.BG_COLOR
HEALTHBAR_COLOR = GameParameters.HEALTHBAR_COLOR
HEALTHBAR_HEIGHT = GameParameters.HEALTHBAR_HEIGHT

SCREEN_WIDTH = GameParameters.SCREEN_WIDTH
SCREEN_HEIGHT = GameParameters.SCREEN_HEIGHT

FRAMERATE = GameParameters.FRAMERATE

NUM_GENERATIONS = GameParameters.NUM_GENERATIONS

class Game:
  def __init__(self):
    self._running = True
    self.screen = None
    self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT

  def on_init(self):
    pygame.init()
    self.screen = pygame.display.set_mode(
      self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    # Fill background and blits everything to the screen
    self.background = pygame.Surface(self.size)
    self.background = self.background.convert()
    self.background.fill(BG_COLOR)
    self.screen.blit(self.background, (0, 0))
    pygame.display.flip()

    self.terrain = Terrain()

    self.beaver = Beaver()
    self.beaversprite = pygame.sprite.RenderPlain(self.beaver)
    self.generationtime = pygame.time.get_ticks()

    self.brain = Brain()
    self.brain.environment.setbeaver(self.beaver)

    self.wolf = Wolf()
    self.wolfsprite = pygame.sprite.RenderPlain(self.wolf)

    self._clock = pygame.time.Clock()
    self._running = True

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False

  def on_loop(self):
    self.beaver.seteyeview(self.terrain.terraingroup)
    self.beaversprite.update()

    self.brain.experiment.doInteractions(1)

    self.wolf.seteyeview(self.terrain.terraingroup)
    self.wolf.setscentview(self.beaver)
    #self.wolfsprite.update()

    marsh = self.terrain.getmarsh()
    if (self.beaver.action == Constants.BEAVER_ACTION_DROP_LUMBER and
        self.beaver.droppedlumber and
        pygame.sprite.collide_rect(self.beaver, marsh)):
      marsh.improve()
    marsh.update()

    # Reset the wolf if it gets stuck in marsh
    if pygame.sprite.collide_rect(self.wolf, marsh):
      self.wolf.respawn()

    if (self.beaver.energy <= 0 or
      self.beaver.rect.colliderect(self.wolf.rect)):

      temp = pygame.time.get_ticks()
      # Only when beaver starves
      if self.beaver.energy <= 0:
        generationtimes.append("%d\t%d" % (self.beaver.generationcount,
                                           temp - self.generationtime))
      self.generationtime = temp

      self.beaver.respawn()
      self.brain.agent.learn()
      self.brain.agent.reset()



      if self.beaver.generationcount > NUM_GENERATIONS:
        self._running = False

      # Reset the wolf so that it seems as if time has passed
      # (aka wolf not lurking around marsh on beaver spawn)
      self.wolf.respawn()

      # Reset the environment so beavers start alike.
      marsh.respawn()
      self.terrain.respawntrees()

    else:
      tree = pygame.sprite.spritecollideany(self.beaver,
        self.terrain.gettreelist())
      if tree is not None and not isinstance(tree, Marsh):
        # Check beaver state
        if self.beaver.action == Constants.BEAVER_ACTION_EAT:
          tree.setstate(Constants.TREE_STATE_ATE)
          tree.update()
        elif (self.beaver.action == Constants.BEAVER_ACTION_PICK_UP_LUMBER and
              self.beaver.pickeduplumber):
          tree.setstate(Constants.TREE_STATE_FORAGED)
          tree.update()

        # Check tree state
        if tree.health <= 0:
          self.terrain.respawntree(tree)

  def on_render(self):
    self.background.fill(BG_COLOR)
    self.screen.blit(self.background, (0, 0))

    # Draws beaver, wolf, marsh, and tree sprites
    self.terrain.terraingroup.draw(self.screen)
    self.beaversprite.draw(self.screen)
    self.wolfsprite.draw(self.screen)

    # Draws energy and health bars of beaver and trees
    bx, by = self.beaver.rect.topleft
    brect = pygame.Rect(bx, by, self.beaver.energybar, HEALTHBAR_HEIGHT)
    pygame.draw.rect(self.screen, HEALTHBAR_COLOR, brect, 0)

    for sprite in self.terrain.terraingroup:
      sx, sy = sprite.rect.topleft
      srect = pygame.Rect(sx, sy, sprite.healthbar, HEALTHBAR_HEIGHT)
      pygame.draw.rect(self.screen, HEALTHBAR_COLOR, srect, 0)

    # Inefficient but works w/o hacking up a blit function for transparent imgs
    pygame.display.update()
    self._clock.tick(FRAMERATE)

  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    while (self._running):
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
    self.on_cleanup()

if __name__ == "__main__":
  generationtimes = []
  game = Game()
  game.on_execute()
  with open('generationtime.txt', 'a') as datafile:
    datafile.write(','.join(generationtimes))
    datafile.write('\n')
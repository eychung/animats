import pygame
from pygame.locals import *
from beaver import Beaver
from marsh import Marsh
from terrain import Terrain
from tree import Tree

BG_COLOR = (0, 92, 9)
HEALTHBAR_COLOR = (0, 255, 0)

class Game:
  def __init__(self):
    self._running = True
    self.screen = None
    self.size = self.weight, self.height = 640, 400

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

    self.beaver = Beaver((0.47, 1))
    self.beaversprite = pygame.sprite.RenderPlain(self.beaver)

    self._clock = pygame.time.Clock()
    self._running = True

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False

  def on_loop(self):
    self.beaver.seteyeview(self.terrain.terraingroup)
    self.beaversprite.update()

    tree = pygame.sprite.spritecollideany(self.beaver,
      self.terrain.gettreelist())
    if tree is not None and not isinstance(tree, Marsh):
      # Check beaver state
      if self.beaver.state == Beaver.CONST_STATE_EAT:
        tree.setstate(Tree.CONST_STATE_ATE)
        tree.update()
      elif self.beaver.state == Beaver.CONST_STATE_FORAGE:
        tree.setstate(Tree.CONST_STATE_FORAGED)
        tree.update()

      # Check tree state
      if tree.health <= 0:
        tree.kill()
        self.beaver.setstate(Beaver.CONST_STATE_WALK_LAND)

  def on_render(self):
    self.background.fill(BG_COLOR)
    self.screen.blit(self.background, (0, 0))

    # Draws beaver, marsh, and tree sprites
    self.terrain.terraingroup.draw(self.screen)
    self.beaversprite.draw(self.screen)

    # Draws energy and health bars of beaver and trees
    bx, by = self.beaver.rect.topleft
    brect = pygame.Rect(bx, by, self.beaver.energybar, 5)
    pygame.draw.rect(self.screen, HEALTHBAR_COLOR, brect, 0)

    for sprite in self.terrain.terraingroup:
      sx, sy = sprite.rect.topleft
      srect = pygame.Rect(sx, sy, sprite.healthbar, 5)
      pygame.draw.rect(self.screen, HEALTHBAR_COLOR, srect, 0)

    # Inefficient but works w/o hacking up a blit function for transparent imgs
    pygame.display.update()
    self._clock.tick(60)

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
  game = Game()
  game.on_execute()


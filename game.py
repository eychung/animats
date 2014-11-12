import pygame
from pygame.locals import *
from beaver import Beaver
from terrain import Terrain
from tree import Tree

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
    self.background.fill((255, 255, 255))
    self.screen.blit(self.background, (0, 0))
    pygame.display.flip()

    self.terraingroup = Terrain()

    self.beaver = Beaver((0.47, 2))
    self.beaversprite = pygame.sprite.RenderPlain(self.beaver)

    self._clock = pygame.time.Clock()
    self._running = True

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False

  def on_loop(self):
    self.beaversprite.update()

  def on_render(self):
    self.background.fill((255, 255, 255))
    self.screen.blit(self.background, (0, 0))

    self.terraingroup.draw(self.screen)
    self.beaversprite.draw(self.screen)

    # Draws energy and health bars of beaver and trees
    bx, by = self.beaver.rect.topleft
    brect = pygame.Rect(bx, by, self.beaver.rect.width, 5)
    pygame.draw.rect(self.screen, (0, 255, 0), brect, 0)

    for sprite in self.terraingroup:
      if isinstance(sprite, Tree):
        sx, sy = sprite.rect.topleft
        srect = pygame.Rect(sx, sy, sprite.rect.width, 5)
        pygame.draw.rect(self.screen, (0, 255, 0), srect, 0)

    # Inefficient but works without hacking up a blit function for transparent images
    pygame.display.update()
    self._clock.tick(10)

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

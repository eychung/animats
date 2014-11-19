import pygame
from pygame.locals import *
from marsh import Marsh
from tree import Tree

initnumtrees = 50

class Terrain(pygame.sprite.Group):
  def __init__(self):
    pygame.sprite.Group.__init__(self)
    screen = pygame.display.get_surface()

    # Add lake
    self.add_internal(Marsh())

    # Add initnumtrees or less trees
    for num in range(initnumtrees):
      tree = Tree()
      while pygame.sprite.spritecollideany(tree, self) is None:
        self.add_internal(tree)

  def gettreelist(self):
    treelist = []
    for sprite in self.sprites():
      if isinstance(sprite, Tree):
        treelist.append(sprite)
    return treelist

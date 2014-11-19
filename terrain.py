import pygame
from pygame.locals import *
from marsh import Marsh
from tree import Tree

initnumtrees = 50

class Terrain:
  def __init__(self):
    screen = pygame.display.get_surface()
    self.terraingroup = pygame.sprite.Group()

    # Add lake
    self.terraingroup.add(Marsh())

    # Add initnumtrees or less trees
    for num in range(initnumtrees):
      tree = Tree()
      while pygame.sprite.spritecollideany(tree, self.terraingroup) is None:
        self.terraingroup.add(tree)

  def gettreelist(self):
    treelist = []
    for sprite in self.terraingroup.sprites():
      if isinstance(sprite, Tree):
        treelist.append(sprite)
    return treelist


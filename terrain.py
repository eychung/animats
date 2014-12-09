import pygame
from pygame.locals import *
from marsh import Marsh
from tree import Tree
from parameters import TerrainParameters

MAX_NUM_TREES = TerrainParameters.MAX_NUM_TREES

class Terrain:
  def __init__(self):
    screen = pygame.display.get_surface()
    self.terraingroup = pygame.sprite.Group()

    # Add lake
    self.terraingroup.add(Marsh())

    # Add initnumtrees or less trees
    for num in range(MAX_NUM_TREES):
      tree = Tree()
      if pygame.sprite.spritecollideany(tree, self.terraingroup) is None:
        self.terraingroup.add(tree)

  def gettreelist(self):
    treelist = []
    for sprite in self.terraingroup.sprites():
      if isinstance(sprite, Tree):
        treelist.append(sprite)
    return treelist

  def getmarsh(self):
    for sprite in self.terraingroup.sprites():
      if isinstance(sprite, Marsh):
        return sprite

  def respawntrees(self):
    for tree in self.gettreelist():
      self.respawntree(tree)

  def respawntree(self, tree):
    tree.respawn()
    sprites = pygame.sprite.spritecollide(tree, self.terraingroup,
                                          False)

    # while it collides with something other than itself
    while len(sprites) > 1:
      tree.respawn()
      sprites = pygame.sprite.spritecollide(
        tree, self.terraingroup, False)
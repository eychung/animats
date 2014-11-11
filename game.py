import pygame
from pygame.locals import *
from beaver import Beaver
from tree import Tree

class Game:
	def __init__(self):
		self._running = True
		self.screen = None
		self.size = self.weight, self.height = 640, 400

	def on_init(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

		# Fill background and blits everything to the screen
		self.background = pygame.Surface(self.size)
		self.background = self.background.convert()
		self.background.fill((255, 255, 255))
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()

		self.treegroup = pygame.sprite.Group()
		for tree in range(20):
			self.treegroup.add(Tree())

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
		self.screen.blit(self.background, self.beaver.rect, self.beaver.rect)
		self.beaversprite.draw(self.screen)
		self.treegroup.draw(self.screen)
		pygame.display.flip()
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

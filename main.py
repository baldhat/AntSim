import pygame

from Renderer import Renderer
from environment.environment import Environment


class App:
    def __init__(self, fps=60):
        self._running = True
        self._pause = False
        self.size = self.width, self.height = 1920, 1020
        self.env = Environment((1700, 1020))
        self.info_panel_size = (self.width - self.env.width, self.height)
        self.info_panel_pos = (self.env.width, 0)
        self.fps = fps
        self.iters_per_second = 0

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Simulation')
        self.renderer = Renderer(self.env, self.size, self.info_panel_size, self.info_panel_pos, fps=self.fps)

    def on_cleanup(self):
        pygame.quit()

    '''
    Initialize and handle the game loop
    '''
    def on_execute(self):
        self.on_init()

        while self._running:
            self.events()
            if not self._pause:
                self.env.step()
            self.renderer.render()
        self.on_cleanup()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._pause = not self._pause
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.renderer.inspected = self.env.get_nearest_actor(event.pos)



if __name__ == "__main__":
    app = App()
    app.on_execute()
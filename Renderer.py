import pygame


class Renderer:
    def __init__(self, env, size, info_panel_size, info_panel_pos, fps=60):
        self.env = env
        self.size = size
        self.fps = fps
        self.info_panel_size = info_panel_size
        self.info_panel_pos = info_panel_pos
        self.screen = pygame.display.set_mode(self.size)
        self.surface = pygame.Surface(self.screen.get_size())
        self.info_panel = pygame.Surface(self.info_panel_size)
        self.env.on_init()
        self.inspected = self.env.actors[0]
        pygame.font.init()
        self.stat_font = pygame.font.SysFont('ubuntu', 17)
        self.caption_font = pygame.font.SysFont('ubuntu', 20, bold=True)
        self.iters_per_second = 0
        self.clock = pygame.time.Clock()

    def render(self):
        self.surface.fill((100, 100, 100))
        self.draw_food_zones()
        self.draw_food()
        self.draw_actors()
        self.draw_info_panel()
        self.iters_per_second = self.iters_per_second * 0.9 + 0.1 * int(1000 / self.clock.tick(self.fps))
        pygame.display.flip()

    def draw_actors(self):
        for actor in self.env.actors:
            pygame.draw.circle(self.surface, actor.color, (int(actor.pos[0]), int(actor.pos[1])), 2)
        self.screen.blit(self.surface.convert(), (0, 0))

    def draw_info_panel(self):
        fw, fh = self.stat_font.size("HeightTest")
        cw, ch = self.caption_font.size("Stats")
        text_pos = lambda x, y: (self.info_panel_pos[0] + 2 + (y * self.info_panel_size[0] / 2),
                                 self.info_panel_pos[1] + x * (fh + 4) + ch + 4)
        # Caption
        self.info_panel.fill((150, 150, 150))
        stats_caption = self.caption_font.render("Stats", True, (0, 0, 0))
        iters_per_second_text = self.stat_font.render(f"{self.iters_per_second:.1f} fps", True, (0, 0, 0))
        actor_num_text = self.stat_font.render("Actors: ", True, (0, 0, 0))
        actor_num = self.stat_font.render(f"{len(self.env.actors)}", True, (0, 0, 0))

        pygame.draw.aaline(self.info_panel, (20, 20, 20), (0, ch * 1.5), (self.info_panel_size[0], ch * 1.5))

        # Actor Info
        energy_text = self.stat_font.render("Energy: ", True, (0, 0, 0))
        energy_value = self.stat_font.render(f"{self.inspected.energy:.2f}", True, (0, 0, 0))
        max_speed_text = self.stat_font.render("Max Speed: ", True, (0, 0, 0))
        max_speed_value = self.stat_font.render(f"{self.inspected.speed:.2f}", True, (0, 0, 0))
        iters_survived_text = self.stat_font.render("Survived: ", True, (0, 0, 0))
        iters_survived_value = self.stat_font.render(f"{self.inspected.num_iters_survived:.2f}", True, (0, 0, 0))

        # Caption
        self.screen.blit(self.info_panel, self.info_panel_pos)
        self.screen.blit(stats_caption, (self.info_panel_pos[0] + 2, self.info_panel_pos[1] + 2))
        self.screen.blit(iters_per_second_text,
                         (self.info_panel_pos[0] + self.info_panel_size[0] -
                          self.stat_font.size(f"{self.iters_per_second:.1f} fps")[0],
                          self.info_panel_pos[1] + 2))
        self.screen.blit(actor_num_text, (self.info_panel_pos[0] + 2, self.info_panel_pos[1] + fh + ch))
        self.screen.blit(actor_num, text_pos(4, 1))

        # Actor Info
        self.screen.blit(energy_text, text_pos(1, 0))
        self.screen.blit(energy_value, text_pos(1, 1))
        self.screen.blit(max_speed_text, text_pos(2, 0))
        self.screen.blit(max_speed_value, text_pos(2, 1))
        self.screen.blit(iters_survived_text, text_pos(3, 0))
        self.screen.blit(iters_survived_value, text_pos(3, 1))

    def draw_food_zones(self):
        for food_zone in self.env.food_zones:
            s = pygame.Surface(food_zone.size)  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((0, 255, 0))  # this fills the entire surface
            self.surface.blit(s, food_zone.pos)
            self.screen.blit(self.surface, food_zone.pos)

    def draw_food(self):
        for food_index in self.env.food_indices:
            pygame.draw.rect(self.surface, (255, 0, 0),
                             (food_index[0], food_index[1], 1, 1), 0)
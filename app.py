import pygame
from random import choice



class Game:
    def __init__(self):
        pygame.init()

        font_name = choice([x for x in pygame.font.get_fonts() if 'cam' in x.lower()])
        self.font_score = pygame.font.SysFont(font_name, 30)
        self.font_info = pygame.font.SysFont(font_name, 50)

        self.running = True
        self.display: pygame.Surface = pygame.display.set_mode((1366, 768))
        pygame.display.set_caption("SpaceInvaders")
        self.screen = pygame.Surface((1920, 1080))
        self.round_tick = 0
        self.clock = pygame.time.Clock()
        self.FPS = 30  # maximální počet FPS

        player_size = (50, 50)
        enemy_size = (60, 60)
        self.missile_size = (10, 20)

        self.player_speed = 10
        self.enemy_speed_orig = 5
        self.missile_speed = -10
        self.missile_cd = 10

        # umisti hrace 1 ze zacatku vlevo doprostred
        self.player_orig = pygame.Rect((self.screen.get_width() // 2, self.screen.get_height() - player_size[1]), player_size)
        # a vytvor jeho kopii, abychom pri kazdem kole se mohli jednoduse vratit k puvodni pozici
        self.player = self.player_orig.copy()
        self.player_score = 0
        self.enemy_score = 0

        # hrace cislo 2 umisti vpravo doprostred
        self.enemy_orig = pygame.Rect(( self.screen.get_width() // 2, 0), enemy_size)
        self.enemy1 = self.enemy_orig.copy()

        self.missiles = []

        self.top = pygame.Rect((0, -self.missile_speed), (self.screen.get_width(), self.missile_speed))
        self.bottom = pygame.Rect((0, self.screen.get_height()), (self.screen.get_width(), self.missile_speed))
        self.left = pygame.Rect((-self.missile_speed, 0), (self.missile_speed, self.screen.get_height()))
        self.right = pygame.Rect((self.screen.get_width(), 0), (self.missile_speed, self.screen.get_height()))

        self.logic = self.logic_game_start

    def create_missiles(self):
        missile = pygame.Rect((self.player.x, self.player.y), self.missile_size)
        self.missiles.append(missile)


    def main(self):
        while self.running:
            # UDALOSTI
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    self.running = False

            
            # KRESLENI
            pygame.draw.rect(self.screen, (255, 255, 255), self.player)
            pygame.draw.rect(self.screen, (255, 0, 0), self.enemy1)

            for missile in self.missiles:
                pygame.draw.rect(self.screen, (0, 0, 255), missile)

            text = self.font_score.render(f"{self.player_score} : {self.enemy_score}", True, (255, 255, 255))
            self.screen.blit(text, ((self.screen.get_width() - text.get_width()) / 2, 0))

            pygame.transform.scale(self.screen, self.display.get_size(), self.display)
            pygame.display.flip()
            self.clock.tick(self.FPS)
            self.screen.fill((0, 0, 0))

            self.logic()
            

    def logic_game_start(self):
        # vykresleni otazky na obrazovku
        text = self.font_info.render("Press SPACE to start the game", True, (255, 255, 255))
        self.screen.blit(text, ((self.screen.get_width() - text.get_width()) / 2,
                                (self.screen.get_height() * 0.75 - text.get_height()) / 2))

        # kontrola odpovedi
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            self.logic = self.logic_round_start

    def logic_round_start(self):
        
        
        self.player = self.player_orig.copy()
        self.enemy1 = self.enemy_orig.copy()
        self.missile_tick = self.missile_cd
        self.enemy_direction = 1
        self.enemy_speed = self.enemy_speed_orig
        self.missiles = []

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            self.logic = self.logic_game_body
        
        # vykresli hlasku pro uzivatele
        text = self.font_info.render("Press SPACE to start", True, (255, 255, 255))
        self.screen.blit(text, ((self.screen.get_width() - text.get_width()) / 2,
                                (self.screen.get_height() * 0.75 - text.get_height()) / 2))

        

        

    def logic_game_body(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.missile_tick > self.missile_cd - 1:
            self.create_missiles()
            self.missile_tick = 0
        self.missile_tick += 1
        if pressed[pygame.K_a] and not self.player.colliderect(self.left):
            self.player.move_ip(-self.player_speed, 0)
        elif pressed[pygame.K_d] and not self.player.colliderect(self.right):
            self.player.move_ip(self.player_speed, 0)

        if self.enemy1.colliderect(self.left):
            self.enemy_direction = 1
        elif self.enemy1.colliderect(self.right):
            self.enemy_direction = -1

        move_x = self.enemy_speed * self.enemy_direction
        move_y = self.enemy_speed
        
        self.enemy1.move_ip(move_x, move_y/5)

        for missile in self.missiles:
            missile.move_ip(0, self.missile_speed)
            if missile.colliderect(self.enemy1):
                self.player_score += 1
                self.logic = self.logic_round_start
            elif missile.colliderect(self.top):
                self.missiles.remove(missile)

        if self.enemy1.colliderect(self.player) or self.enemy1.colliderect(self.bottom):
            self.enemy_score += 1
            self.logic = self.logic_round_start

        if self.round_tick > 0 and self.round_tick % (2 * self.FPS) == 0:
            self.enemy_speed = min(1.1 * self.enemy_speed, 20)
        self.round_tick += 1


if __name__ == '__main__':
    Game().main()
        



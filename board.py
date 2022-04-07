import pygame
import sys
import pygame.font

from pygame.locals import *
from CONST import *
class Board():
    def __init__(self, game, x_player, o_player):
        pygame.init()
        self.game = game
        self.load_images()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.click = False
        self.moves = 0
        self.print_board(game)

    def load_images(self):
        self.ximage = pygame.image.load('img/x.png')
        self.ximage = pygame.transform.scale(self.ximage, (FS, FS))
        self.oimage = pygame.image.load('img/o.png')
        self.oimage = pygame.transform.scale(self.oimage, (FS, FS))

    def draw_text(self, text, font_size, color, x, y):
        font = pygame.font.Font(None, font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def print_board(self, game):
        while True:
            self.screen.fill(BLACK)
            self.display_board()

            winner = self.who_win()
            if winner is None:
                sgn = 'O' if self.moves % 2 else 'X'
                text = sgn + "'s turn!"
                #self.update_board()
            elif winner == 'tie':
                text = "Tie!"
            else:
                #self.draw_line(winner)
                text = winner + " won!"

            if self.moves % 2:
                self.update_board()
            else:
                self.AImove()

            self.draw_text(text, 50, WHITE, (FS * 3 + GS * 2)/2, US/2)

            mx, my = pygame.mouse.get_pos()

            button1 = pygame.Rect(50, US + FS * 3 + GS * 2 + 30, 200, 50)
            button2 = pygame.Rect(50, 200, 200, 50)
            button3 = pygame.Rect(50, 300, 200, 50)

            if button1.collidepoint((mx,my)):
                if self.click:
                    print("siemanko")
                    self.reset_game()
            if button2.collidepoint((mx, my)):
                if self.click:
                    pass
            if button3.collidepoint((mx, my)):
                if self.click:
                    pass

            pygame.draw.rect(self.screen, (255, 0, 0), button1)

            self.click = False
            self.check_events()

            pygame.display.update()
            self.clock.tick(60)

    def display_board(self):
        for i in range(3):
            for j in range(3):
                 if self.fields[i][j] == "":
                     field = pygame.Rect((FS + GS) * j, (FS + GS) * i + US, FS, FS)
                     pygame.draw.rect(self.screen, WHITE, field)
        # for i in range(3):
        #     for j in range(3):
        #         if self.fields[i][j] == "":
        #             field = pygame.Rect((FS + GS) * j, (FS + GS) * i + US, FS, FS)
        #             pygame.draw.rect(self.screen, WHITE, field)
        #         elif self.fields[i][j] == "X":
        #             self.screen.blit(self.ximage, ((FS + GS) * j, (FS + GS) * i + US))
        #         else:
        #             self.screen.blit(self.oimage, ((FS + GS) * j, (FS + GS) * i + US))

    def reset_game(self):
        self.moves = 0
        self.game.board = self.game.make_board()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def close(self):
        pygame.quit()
        sys.exit()
import pygame
import sys
import pygame.font
from pygame.locals import *
from CONST import *


class TicTacToe:
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

        self.x_image = pygame.image.load('img/x.png')
        self.x_image = pygame.transform.scale(self.x_image, (FS * 0.76, FS * 0.76))
        self.o_image = pygame.image.load('img/o.png')
        self.o_image = pygame.transform.scale(self.o_image, (FS * 0.76, FS * 0.76))
        self.background_image = pygame.image.load('img/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (FS * 3 + 2 * GS, FS * 3 + 2 * GS))

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.click = False
        pygame.init()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                print("close")
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    @staticmethod
    def close():
        pygame.quit()
        sys.exit()

    def display_board(self):
        self.screen.blit(self.background_image, (0, US))
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "X":
                    self.screen.blit(self.x_image, ((FS + GS) * j + FS * 0.12, (FS + GS) * i + US + FS * 0.12))
                elif self.board[i][j] == "O":
                    self.screen.blit(self.o_image, ((FS + GS) * j + FS * 0.12, (FS + GS) * i + US + FS * 0.12))

    def draw_text(self, text, font_size, color, x, y):
        font = pygame.font.Font(None, font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    @staticmethod
    def make_board():
        return [[" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]]

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square[0]][square[1]] == ' ':
            self.board[square[0]][square[1]] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row = self.board[square[0]]
        if all([s == letter for s in row]):
            return True

        column = [self.board[i][square[1]] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        diagonal1 = [self.board[i][i] for i in range(3)]
        if all([s == letter for s in diagonal1]):
            return True

        diagonal1 = [self.board[2-i][i] for i in range(3)]
        if all([s == letter for s in diagonal1]):
            return True

        return False

    def num_empty_squares(self):  # counts number of empty squares in board
        num = 0
        for row in self.board:
            num += row.count(' ')
        return num

    def available_moves(self):  # returns list of available moves
        res = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    res.append((i, j))
        return res

    def reset_game(self):
        self.board = self.make_board()
        self.current_winner = None


def play(game, o_player, x_player, print_game=True):
    letter = o_player.letter
    while True:
        game.screen.fill(BLACK)
        game.display_board()

        if game.current_winner is None and not game.available_moves():
            text = 'Tie!'
        elif game.current_winner is not None:
            text = game.current_winner + " won!"
        else:
            text = letter + "'s turn!"

        game.draw_text(text, 50, WHITE, (FS * 3 + GS * 2) / 2, US / 2)

        if letter == "O":
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if square is not None:
            if game.make_move(square, letter):
                if print_game:
                    print(letter + ' makes a move to square {}'.format(square))
                    game.print_board()
                    print('')

                if game.current_winner:
                    if print_game:
                        print(letter + ' wins!')

                letter = 'O' if letter == 'X' else 'X'  # switches player

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect((FS*3 + GS*2 - 200)/2, US + FS * 3 + GS * 2 + (LS - 50)/2, 200, 50)

        if button1.collidepoint((mx, my)):
            if game.click:
                game.reset_game()

        pygame.draw.rect(game.screen, RED, button1)
        game.draw_text("reset", 50, WHITE, (FS*3 + GS*2)/2, US + 3*FS + 2*GS + LS/2)

        game.click = False
        game.check_events()

        pygame.display.update()
        game.clock.tick(60)

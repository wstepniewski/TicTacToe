import math
import random
import pygame
from CONST import *


class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        mx, my = pygame.mouse.get_pos()

        if game.click:
            i = (my - US) // (FS + GS)
            j = mx // (FS + GS)
            print(mx, my)
            if i in range(0, 3) and j <= 2 and game.board[i][j] == " ":
                return i, j
        return None


class RandomPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class SmartPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            square = random.choice(corners)
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.num_empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}
        for move in state.available_moves():
            state.make_move(move, player)
            sim_score = self.minimax(state, other_player)

            # undo move
            state.board[move[0]][move[1]] = ' '
            state.current_winner = None

            sim_score['position'] = move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

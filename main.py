import game
from player import HumanPlayer, RandomPlayer, SmartPlayer

if __name__ == '__main__':
    x_player = SmartPlayer('X')
    #o_player = SmartPlayer('O')
    o_player = HumanPlayer('O')
    #x_player = HumanPlayer('X')
    #x_player = RandomPlayer('X')
    t = game.TicTacToe()
    game.play(t, o_player, x_player, print_game=True)

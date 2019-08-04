import numpy as np
from .WonDevLogic import Board


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanWonDevPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        pi = [x[0] for x in filter(lambda x: x[1],zip(range(len(valid)-1),valid))]

        for i in range(len(pi)):
            (playerid, action, dir1, dir2) = Board.decode_move(pi[i])
            dir1 = Board.directions[dir1]
            dir2 = Board.directions[dir2]
            print(i, ': ', (playerid, action, dir1, dir2))

        if (len(pi) == 0):
            print(len(valid)-1, ': pass')

        while True:
            try:
                a = int(input().lstrip().rstrip())
                if(len(pi) != 0): 
                    a = pi[a]

                if valid[a]:
                    return a
            except:
                pass

            print('Invalid')


class GreedyWonDevPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]

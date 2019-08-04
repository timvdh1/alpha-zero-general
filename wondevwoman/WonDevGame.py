from __future__ import print_function
import sys
#sys.path.append('..')
from Game import Game
from .WonDevLogic import Board
import numpy as np


class WonDevGame(Game):
    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.tiles)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return (1 * 2 * 8 * 8) + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move

        if action == self.getActionSize()-1:
            return (board, -player)

        b = Board(self.n)
        b.tiles = np.copy(board)
        b.towerTiles = b.tiles[0]
        b.playerTiles = b.tiles[1]
        b.scoreTiles = b.tiles[2]
        b.execute_move(action, player)
        return (b.tiles, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.tiles = np.copy(board)
        b.towerTiles = b.tiles[0]
        b.playerTiles = b.tiles[1]
        b.scoreTiles = b.tiles[2]
        legalMoves =  b.get_legal_moves(player)

        for m in legalMoves:
            valids[m]=1

        if(len(legalMoves) == 0):
            valids[-1] = 1

        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.tiles = np.copy(board)
        b.towerTiles = b.tiles[0]
        b.playerTiles = b.tiles[1]
        b.scoreTiles = b.tiles[2]
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        
        count = b.countDiff(player)
        if count > 0:
            return 1
        elif count == 0:
            return 0.5
        else:
            return -1

    def getCanonicalForm(self, board, player):
        tiles = np.copy(board)
        tiles[1] *= player
        tiles[2] *= player
        # return state if player==1, else return -state if player==-1
        return tiles

    def getSymmetries(self, board, pi):
        # mirror, rotational      
        l = []
        
        pi_len = len(pi)
        pi = [x[0] for x in filter(lambda x: x[1],zip(range(pi_len-1),pi))]
        
        for i in range(1, 5):
            for j in [True, False]:
                newB1 = np.rot90(board[0], i)
                newB2 = np.rot90(board[1], i)
                newB3 = np.rot90(board[2], i)
                
                newPi = [None]*pi_len        
                for move in pi:
                    (playerid, action, dir1, dir2) = Board.decode_move(move)
                    playerid -= 1
                    dir1 = (dir1+(6 if j else 2))%8
                    dir2 = (dir2+(6 if j else 2))%8
                    newPi[playerid*(2*8*8)+action*(8*8)+dir1*(8)+dir2] = 1

                if j:
                    newB1 = np.fliplr(newB1)
                    newB2 = np.fliplr(newB2)  
                    newB2 = np.fliplr(newB3)                  

                l += [(np.array([newB1,newB2,newB3]), newPi)]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    def getScore(self, board, player):
        b = Board(self.n)
        b.tiles = np.copy(board)
        b.towerTiles = b.tiles[0]
        b.playerTiles = b.tiles[1]
        b.scoreTiles = b.tiles[2]
        return b.countDiff(player)

def display(board):
    print(board)
    import time
    #time.sleep(1)
    return
    n = board.shape[1]

    for y in range(n):
        print (y,"|",end="")
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|",end="")    # print the row #
        for x in range(n):
            if(board[1][y][x]):
                piece = board[0][y][x]    # get the piece to print
                print(board[1][y][x],"x",end="")
            else:   
                piece = board[0][y][x]    # get the piece to print
                print(0," ",end="")
            
        print("|")
    print("   -----------------------")

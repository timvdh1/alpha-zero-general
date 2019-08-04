'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     towerTiles[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

sign = lambda x: x and (1, -1)[x < 0]

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.tiles = [None]*3

        self.towerTiles = self.tiles[0] = [None]*self.n
        self.playerTiles = self.tiles[1] = [None]*self.n
        self.scoreTiles = self.tiles[2] = [None]*self.n
        for i in range(self.n):
            self.towerTiles[i] = [0]*self.n
            self.playerTiles[i] = [0]*self.n
            self.scoreTiles[i] = [0]*self.n

        # Set up the initial 4 towerTiles.
        self.playerTiles[int(self.n/2)-1][int(self.n/2)-1] = 1
        self.playerTiles[int(self.n/2)][int(self.n/2)] = -1

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with towerTiles of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if sign(self.playerTiles[x][y])==color:
                    newmoves = self.get_moves_for_square((x,y))
                    playerid = (abs(self.playerTiles[x][y])-1) * (2 * 8 * 8)
                    newmoves = map(lambda move: (playerid+move) , newmoves)
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if sign(self.playerTiles[x][y])==color:
                    newmoves = self.get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white towerTiles, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        # search all possible directions.
        moves = []
        mid = 0
        for moveDirection in Board.directions:
            move = self._discover_move(square, moveDirection)
            if move:
                bid = 0
                for buildDirection in Board.directions:
                    build = self._discover_build(move, buildDirection)
                    if(build):
                        moves.append(mid*8+bid)
                    bid += 1            
            mid += 1

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board; flips towerTiles as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (playerid, action, dir1, dir2) = self.decode_move(move)
        playerid *= sign(color)
        dir1 = Board.directions[dir1]
        dir2 = Board.directions[dir2]        

        for y in range(self.n):
            for x in range(self.n):
                if self.playerTiles[x][y]==playerid:
                    if(action == 0): #build
                        self.playerTiles[x + dir1[0]][y + dir1[1]] = self.playerTiles[x][y]
                        self.playerTiles[x][y] = 0
                        x += dir1[0]
                        y += dir1[1]
                        self.towerTiles[x + dir2[0]][y + dir2[1]] += 1
                        if(self.towerTiles[x][y] == 3):
                            self.scoreTiles[x][y] += color
                        return
                    else:       #push
                        self.playerTiles[x + dir1[0] + dir2[0]][y + dir1[1] + dir2[1]] = self.playerTiles[x + dir1[0]][y + dir1[1]]
                        self.playerTiles[x + dir1[0]][y + dir1[1]] = 0
                        self.towerTiles[x + dir1[0]][y + dir1[1]] += 1
                        return

    @staticmethod
    def decode_move(move):
        playerid = move // (2 * 8 * 8)
        move = move % (2 * 8 * 8)

        action = move // (8 * 8)
        move = move % (8 * 8)

        dir1 = move // (8)
        dir2 = move % (8)

        return (playerid + 1, action, dir1, dir2)

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        height = self.towerTiles[x][y]

        dx, dy = direction
        target = (x+dx,y+dy)
        if(not (target[0] < 0 or target[0] >= self.n or target[1] < 0 or target[1] >= self.n)):    
            theight = self.towerTiles[target[0]][target[1]]            
            if(theight < 4 and theight <= height+1 and self.playerTiles[target[0]][target[1]] == 0):                            
                return target
            
        return None

    def _discover_build(self, origin, direction):   
        x, y = origin    
        dx, dy = direction
        target = (x+dx,y+dy)
        if(not (target[0] < 0 or target[0] >= self.n or target[1] < 0 or target[1] >= self.n)): 
            theight = self.towerTiles[x+dx][y+dy]
            if(theight < 4): 
                return direction
            
        return None

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                count += self.scoreTiles[x][y]
        
        return count * color
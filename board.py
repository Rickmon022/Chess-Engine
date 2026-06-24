import numpy as np

class Board():
    def __init__(self):
        self.board = np.array(
                             [[-4,-2,-3,-5,-6,-3,-2,-4],
                              [-1,-1,-1,-1,-1,-1,-1,-1],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0],
                              [1,1,1,1,1,1,1,1],
                              [4,2,3,5,6,3,2,4]
                              ])
        self.pieces = {}
        for i in range(1,7):
            if i == 1:
                piece = 'p'
            elif i == 2:
                piece = 'N'
            elif i == 3:
                piece = 'B'
            elif i == 4:
                piece = 'R'
            elif i == 5:
                piece = 'Q'
            else:
                piece = 'K'
            self.pieces[i] = 'w'+piece
            self.pieces[-i] = 'b'+piece
        
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startSq[0], move.startSq[1]] = 0
        self.board[move.endSq[0], move.endSq[1]] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

class Move():
    ranksToRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startSq = startSq
        self.endSq = endSq
        self.pieceMoved = board[startSq[0],startSq[1]]
        self.pieceCaptured = board[endSq[0], endSq[1]]

    def getChessNotation(self):
        return self.getRankFile(self.startSq[0], self.startSq[1]) + self.getRankFile(self.endSq[0], self.endSq[1])

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
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

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startSq[0], move.startSq[1]] = move.pieceMoved
            self.board[move.endSq[0], move.endSq[1]] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c]
                if (turn < 0 and not self.whiteToMove) or (turn > 0 and self.whiteToMove):
                    piece = abs(turn)
                    if piece == 1:
                        self.getPawnMoves(r, c, moves)
                    elif piece == 2:
                        self.getKnightMoves(r, c, moves)
                    elif piece == 3:
                        self.getBishopMoves(r, c, moves)
                    elif piece == 4:
                        self.getRookMoves(r, c, moves)
                    elif piece == 5:
                        self.getQueenMoves(r, c, moves)
                    elif piece == 6:
                        self.getKingMoves(r, c, moves)
        return moves
        
    def getPawnMoves(self, r, c, moves):
        pass

    def getKnightMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass

    def getRookMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass

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
        self.moveId = self.startSq[0] * 1000 + self.startSq[1] * 100 + self.endSq[0] * 10 + self.endSq[1]

    def __eq__(self, other):
        if(isinstance(other, Move)):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startSq[0], self.startSq[1]) + self.getRankFile(self.endSq[0], self.endSq[1])

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
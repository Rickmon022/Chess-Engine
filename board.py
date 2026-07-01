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
        # king's position
        self.blackKingPos = (0,4)
        self.whiteKingPos = (7,4)
        self.checkmate = False
        self.stalemate = True

    def makeMove(self, move):
        self.board[move.startSq[0], move.startSq[1]] = 0
        self.board[move.endSq[0], move.endSq[1]] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 6:
            self.whiteKingPos = move.endSq
        elif move.pieceMoved == -6:
            self.blackKingPos = move.endSq

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startSq[0], move.startSq[1]] = move.pieceMoved
            self.board[move.endSq[0], move.endSq[1]] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 6:
                self.whiteKingPos = move.startSq
            elif move.pieceMoved == -6:
                self.blackKingPos = move.startSq

    def getValidMoves(self):
        # 1. generating all possible moves
        moves = self.getAllPossibleMoves()
        # 2. for each move, making the move
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove # checking from opponents side
            if self.inCheck():
                moves.pop(i)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.sqUnderAttack(self.whiteKingPos[0], self.whiteKingPos[1])
        else:
            return self.sqUnderAttack(self.blackKingPos[0], self.blackKingPos[1])
        
    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        
        for move in oppMoves:
            if move.endSq == (r,c):
                return True
        return False

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
        if self.whiteToMove:
            if self.board[r-1][c] == 0:
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == 0:
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c - 1 >= 0:
                if self.board[r-1][c-1] < 0:
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c + 1 <= 7:
                if self.board[r-1][c+1] < 0:
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        else:
            if self.board[r+1][c] == 0:
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == 0:
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c - 1 >= 0:
                if self.board[r+1][c-1] > 0:
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if c + 1 <= 7:
                if self.board[r+1][c+1] > 0:
                    moves.append(Move((r,c), (r+1,c+1), self.board))

    def getKnightMoves(self, r, c, moves):
        KnightMoves = ((-2,-1),(-2,1),(2,1),(2,-1),(1,2),(-1,2),(-1,-2),(1,-2))
        allyColor = "w" if self.whiteToMove else "b"

        for m in KnightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPieceColor = "empty"
                if(self.board[endRow][endCol] < 0): endPieceColor = "b"
                elif(self.board[endRow][endCol] > 0): endPieceColor = "w"
                if endPieceColor != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            i = 1
            while(r+i <= 7 and c+i <= 7 and self.board[r+i][c+i] <= 0):
                moves.append(Move((r,c), (r+i,c+i), self.board))
                if(self.board[r+i][c+i] < 0):
                    break
                i+=1
            i = 1
            while(r+i <= 7 and c-i >= 0 and self.board[r+i][c-i] <= 0):
                moves.append(Move((r,c), (r+i,c-i), self.board))
                if(self.board[r+i][c-i] < 0):
                    break
                i+=1
            i = 1
            while(r-i >= 0 and c-i >= 0 and self.board[r-i][c-i] <= 0):
                moves.append(Move((r,c), (r-i,c-i), self.board))
                if(self.board[r-i][c-i] < 0):
                    break
                i+=1
            i = 1
            while(r-i >= 0 and c+i <= 7 and self.board[r-i][c+i] <= 0):
                moves.append(Move((r,c), (r-i,c+i), self.board))
                if(self.board[r-i][c+i] < 0):
                    break
                i+=1
        else:
            i = 1
            while(r+i <= 7 and c+i <= 7 and self.board[r+i][c+i] >= 0):
                moves.append(Move((r,c), (r+i,c+i), self.board))
                if(self.board[r+i][c+i] > 0):
                    break
                i+=1
            i = 1
            while(r+i <= 7 and c-i >= 0 and self.board[r+i][c-i] >= 0):
                moves.append(Move((r,c), (r+i,c-i), self.board))
                if(self.board[r+i][c-i] > 0):
                    break
                i+=1
            i = 1
            while(r-i >= 0 and c-i >= 0 and self.board[r-i][c-i] >= 0):
                moves.append(Move((r,c), (r-i,c-i), self.board))
                if(self.board[r-i][c-i] > 0):
                    break
                i+=1
            i = 1
            while(r-i >= 0 and c+i <= 7 and self.board[r-i][c+i] >= 0):
                moves.append(Move((r,c), (r-i,c+i), self.board))
                if(self.board[r-i][c+i] > 0):
                    break
                i+=1

    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            i = r+1
            while(i <= 7 and self.board[i][c] <= 0):
                moves.append(Move((r,c), (i,c), self.board))
                if(self.board[i][c] < 0):
                    break
                i+=1
            i = r-1
            while(i >= 0 and self.board[i][c] <= 0):
                moves.append(Move((r,c), (i,c), self.board))
                if(self.board[i][c] < 0):
                    break
                i-=1
            i = c-1
            while(i >= 0 and self.board[r][i] <= 0):
                moves.append(Move((r,c), (r,i), self.board))
                if(self.board[r][i] < 0):
                    break
                i-=1
            i = c+1
            while(i <= 7 and self.board[r][i] <= 0):
                moves.append(Move((r,c), (r,i), self.board))
                if(self.board[r][i] < 0):
                    break
                i+=1
        else:
            i = r+1
            while(i <= 7 and self.board[i][c] >= 0):
                moves.append(Move((r,c), (i,c), self.board))
                if(self.board[i][c] > 0):
                    break
                i+=1
            i = r-1
            while(i >= 0 and self.board[i][c] >= 0):
                moves.append(Move((r,c), (i,c), self.board))
                if(self.board[i][c] > 0):
                    break
                i-=1
            i = c-1
            while(i >= 0 and self.board[r][i] >= 0):
                moves.append(Move((r,c), (r,i), self.board))
                if(self.board[r][i] > 0):
                    break
                i-=1
            i = c+1
            while(i <= 7 and self.board[r][i] >= 0):
                moves.append(Move((r,c), (r,i), self.board))
                if(self.board[r][i] > 0):
                    break
                i+=1

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1),(-1,0),(1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1))
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPieceColor = "empty"
                if(self.board[endRow][endCol] < 0): endPieceColor = "b"
                elif(self.board[endRow][endCol] > 0): endPieceColor = "w"
                if endPieceColor != allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))

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
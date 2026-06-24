import pygame as p
import board

WIDTH = HEIGHT = 512
DIM = 8
SQ_SIZE = HEIGHT//DIM
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ['bB', 'bK', 'bN', 'bQ', 'bp', 'bR', 'wB', 'wK', 'wN', 'wQ', 'wR', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"assets/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs):
    drawSqColors(screen)
    drawPieces(screen, gs.board, gs.pieces)

def drawSqColors(screen):
    colors = [p.Color("white"), p.Color('gray')]
    for r in range(DIM):
        for c in range(DIM):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board, pieces):
    for r in range(DIM):
        for c in range(DIM):
            piece = board[r][c]
            if piece != 0:
                screen.blit(IMAGES[pieces[piece]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    load_images()
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = board.Board()

    sqSelected = ()
    playerClicks = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                col = loc[0]//SQ_SIZE
                row = loc[1]//SQ_SIZE
                if sqSelected == (row, col): # deselect
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append((row, col))
                if len(playerClicks) == 2:
                    move = board.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == '__main__':
    main()
import pygame
from Chess.Board import Board

class Chess_Game:
    def __init__(self, board_size):
        pygame.init()
        self.board_size = board_size
        self.mode = 8
        self.running = True
        self.selected = False
        self.screen = pygame.display.set_mode((self.board_size, self.board_size))
        self.Chess_Board = Board(self.screen, board_size)
        self.main()
        
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #TODO Highlight available moves/selected square
                        row, col = self.get_mouse_position(pygame.mouse.get_pos())
                        selected_square = self.Chess_Board.board[row][col]
                        if selected_square in ("0","x") and self.selected == False:
                            print("select correct square")
                        elif self.selected == False and selected_square not in ("0","x"):
                            self.selected = selected_square
                            print("selected: ", selected_square)
                            print("Valid Moves: ", self.selected.ValidMoves(self.Chess_Board))
                        elif self.selected == selected_square:
                            print("deselected: ", selected_square)
                            self.selected = False
                        elif (row, col) in self.selected.ValidMoves(self.Chess_Board):
                            self.Chess_Board.Move(self.selected.position(), (row, col))
                            self.selected = False
                        else:
                            print("select correct square")
        pygame.quit()
    def get_mouse_position(self, pos):
        x, y = pos
        return y//(self.board_size//self.mode), x//(self.board_size//self.mode)
    
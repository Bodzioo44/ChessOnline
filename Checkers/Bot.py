from copy import deepcopy
from Chess.assets.constants import Color
import random

class Bot:
    def __init__(self, board, color, depth = 4):
        self.depth = depth
        self.board = board
        
        if color == Color.WHITE:
            self.main_color = Color.WHITE
            self.secondary_color = Color.BLACK
        else:
            self.main_color = Color.BLACK
            self.secondary_color = Color.WHITE

    def __repr__(self):
        return f"<{self.main_color.name} {self.__class__.__name__} with depth of: {self.depth}>"

    def GetBotColor(self):
        return self.main_color
    
    def GetBotMove(self, board):
        #return self.MiniMax(board, self.depth, True)[1]
        return self.AlphaBeta(board, self.depth, float('-inf'), float('inf'), True)[1]

    #classic minimax
    def MiniMax(self, board, depth, max_p):
        if depth == 0 or board.CheckForWinner():
            return board.Evaluate(self.main_color), board

        if max_p:
            maxEval = float('-inf')
            best_move = None
            for move in self.Get_Moves(board, self.main_color):
                eval = self.MiniMax(move, depth-1, False)[0]
                maxEval = max(maxEval, eval)
                if maxEval == eval:
                    best_move = move
            return maxEval, best_move

        else:
            minEval = float('inf')
            best_move = None
            for move in self.Get_Moves(board, self.secondary_color):
                eval = self.MiniMax(move, depth-1, True)[0]
                minEval = min(minEval, eval)
                if minEval == eval:
                    best_move = move
            return minEval, best_move
        
    #minimax with alpha beta pruning
    def AlphaBeta(self, board, depth, alpha, beta, max_p):
        if depth == 0 or board.CheckForWinner():
            return board.Evaluate(self.main_color), board

        if max_p:
            maxEval = float("-inf")
            best_move = None
            for move in self.Get_Moves(board, self.main_color):
                eval = self.AlphaBeta(move, depth-1, alpha, beta, False)[0]
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                if maxEval >= beta:
                    break
                alpha = max(alpha, maxEval)

            return maxEval, best_move
        else:
            minEval = float("inf")
            best_move = None
            for move in self.Get_Moves(board, self.secondary_color):
                eval = self.AlphaBeta(move, depth-1, alpha, beta, True)[0]
                if eval < minEval:
                    minEval = eval
                    best_move = move
                if minEval <= alpha:
                    break
                beta = min(beta, minEval)

            return minEval, best_move
        
    def Simulate_Move(self, piece, move, board, nuked):
        board.Move(piece, move)
        for piece in nuked:
            board.Remove(piece)
        return board

    def Get_Moves(self, board, color):
        moves = []
        for piece in board.Grab_All_Pieces(color):
            valid_moves = board.Valid_moves(piece) 
            for move, nuked in valid_moves.items():
                temp_board = deepcopy(board)
                temp_piece = deepcopy(piece)
                #TODO its working, but temp_piece isnt inside temp_board?
                #Nvm, later on its moved and reassigned again anyway
                new = self.Simulate_Move(temp_piece, move, temp_board, nuked)
                moves.append(new)
        
        #list shuffle so games arent repeatable
        random.shuffle(moves)
        return moves
    
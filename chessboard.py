import numpy as np


class ChessBoard():
    def __init__(self, queens):
        # initialized by a list of integers which is locations of queens. range of 0 to 7
        self.board = np.zeros((8, 8))
        self.queens = queens
        for i in range(0,8):
            self.board[queens[i], i] = 1

    def nonattacking_queens(self, r, c):
        # will return how many queens are attacking current position. row and column
        # if in same column, row, diagonal
        attackers = 0

        in_column = sum(self.board[:, c]) - 1
        in_row = sum(self.board[r,:]) - 1
        in_trace = self.board.trace(offset=c-r) - 1 # using the trace of that diagonal

        # using trace of flipped matrix to get opposite diagonals
        flipped_board = np.flip(self.board, 1)
        in_flip_trace = flipped_board.trace(offset=7-r-c) - 1 # 7 is max length - 1

        attackers = int(in_row + in_column + in_trace + in_flip_trace)
        return 4 - attackers # for a total of 4 possible attackers (can technically be lower than 0)

    def fitness_fn(self):
        # number of nonattacking queens. higher results are better. max
        total_fitness = 0
        for r in self.queens:
            total_fitness += self.nonattacking_queens(r, self.queens.index(r))
        return total_fitness
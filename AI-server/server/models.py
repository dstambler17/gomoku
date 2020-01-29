from server.errorHandler.errors import *
import uuid
import time
from random import randrange

class Evaluator:
    #Check if player has 5 pawns in row
    @staticmethod
    def EvalRow(color, board):
        value = 0
        maxValue = 0
        for row in range(19):
            maxValue = value if value > maxValue else maxValue
            value = 0
            for col in range(19):
                if board[row][col] != color:
                    maxValue = value if value > maxValue else maxValue
                    value = 0
                else:
                    value += 1
        return maxValue


    #Check if player has 5 pawns in column
    @staticmethod
    def EvalCol(color, board):
        value = 0
        maxValue = 0
        for col in range(19):
            maxValue = value if value > maxValue else maxValue
            value = 0
            for row in range(19):
                if board[row][col] != color:
                    maxValue = value if value > maxValue else maxValue
                    value = 0
                else:
                    value += 1
        return maxValue


    #Check if player has 5 pawns in diagonal from top left to bottom right
    @staticmethod
    def EvalDiagDownRight(color, board):
        val = 0
        maxVal = 0
        for col in range(15):
            for row in range(15):
                maxVal = val if val > maxVal else maxVal
                val = 0
                for i in range(5):
                    if color != board[row + i][col + i]:
                        maxVal = val if val > maxVal else maxVal
                        val = 0
                    else:
                        val += 1
        return maxVal


    #Check if player has 5 pawns in diagonal from top right to bottom left
    @staticmethod
    def EvalDiagUpRight(color, board):
        val = 0
        maxVal = 0
        for col in range(4, 19):
            for row in range(15):
                maxVal = val if val > maxVal else maxVal
                val = 0
                for i in range(5):
                    if color != board[row + i][col - i]:
                        maxVal = val if val > maxVal else maxVal
                        val = 0
                    else:
                        val += 1
        return maxVal

    @staticmethod
    def evaluate_position(color, board):
        '''
        The idea is to serve as an eval function for the minimax algorithm
        '''
        points = [Evaluator.EvalCol(color, board), Evaluator.EvalRow(color, board), Evaluator.EvalDiagDownRight(color, board), Evaluator.EvalDiagUpRight(color, board)]
        if 5 in points:
            return 100 #This means, the player wins
        double_cut_check = 0
        for point in points:
            if point == 4:
                double_cut_check += 1
        if double_cut_check >= 2:
            return 10 #This means pinsir and thus next move wins
        else:
            return max(points)





class Game():
    def __init__(self, d=None):
        board = []
        '''Add each board row here'''
        for x in range(0,19):
            board.append([''] * 19)

        self.board = board
        self.move = 0
        self.playerColor = ''
        self.winner = None
        self.gameOver = False
        self.gameID = str(uuid.uuid4())

        #option to initialize object from dict
        if d is not None:
            for key in d:
                setattr(self, key, d[key])


    def makeMove(self, x, y):
        '''Get the row at pos x'''
        if self.board[x][y] == '':
            self.board[x][y] = 'white'
            self.move = self.move + 1
        else:
            raise ValidationFailed

    '''MAKE AI MOVE'''
    def makeAIMove(self, x, y):
        if self.move <= 1: #make random first move
            row = randrange(19)
            col = randrange(19)
            if self.board[row][col] == 'white':
                col += 1
            self.board[row][col] = 'black'
            return row, col
        '''
        Implementing the Minimax algo
        '''
        #1.Implement eval for diagonal DONE
        #2. Add test endpoint DONE
        #3. Test eval DONE
        #4. Loop through initial move
        #5. Add minimizer loop

        #maximizer:
        max_move_tuple = (-100,0,0)
        start = time.time()
        for i in range(19):
            for j in range(19):
                if self.board[i][j] == '':
                    self.board[i][j] = 'black'
                    #minimizer:
                    min_move_tuple = (100, 0, 0)
                    for x in range(19):
                        print(x)
                        for y in range(19):
                            if self.board[x][y] == '':
                                self.board[x][y] = 'white'
                                score_black = Evaluator.evaluate_position('black', self.board)
                                if self.move >= 4: #check just to help enhance speed at start of game
                                    score_white = (Evaluator.evaluate_position('white', self.board) * -1) + 1
                                    score = score_black if (score_black + score_white) > 0 else score_white
                                else:
                                    score = score_black
                                if score < min_move_tuple[0]:
                                    min_move_tuple = (score, x, y)
                                self.board[x][y] = ''
                                if min_move_tuple[0] < max_move_tuple[0]:
                                    break
                        if min_move_tuple[0] < max_move_tuple[0]:
                            break
                    self.board[i][j] = ''
                    if min_move_tuple[0] > max_move_tuple[0]:
                        max_move_tuple = (min_move_tuple[0], i, j)
        print(max_move_tuple)
        end = time.time()
        print('Evaluation time: {}s'.format(round(end - start, 7)))
        self.board[max_move_tuple[1]][max_move_tuple[2]] = 'black'
        return max_move_tuple[1], max_move_tuple[2]



    #Check if player has 5 pawns in row
    def checkRow(self, color):
        value = 0
        for row in range(19):
            value = 0
            for col in range(19):
                if self.board[row][col] != color:
                    value = 0
                else:
                    value += 1
                if value == 5:
                    self.Win(color)
                    return


    #Check if player has 5 pawns in column
    def checkCol(self, color):
        value = 0
        for col in range(19):
            value = 0
            for row in range(19):
                if self.board[row][col] != color:
                    value = 0
                else:
                    value += 1
                if value == 5:
                    self.Win(color)
                    return


    #Check if player has 5 pawns in diagonal from top left to bottom right
    def checkDiagDownRight(self, color):
        for col in range(15):
            for row in range(15):
                match = True
                for i in range(5):
                    if color != self.board[row + i][col + i]:
                        match = False
                if match:
                    self.Win(color)
                    return


    #Check if player has 5 pawns in diagonal from top right to bottom left
    def checkDiagUpRight(self, color):
        for col in range(4, 19):
            for row in range(15):
                match = True
                for i in range(5):
                    if color != self.board[row + i][col - i]:
                        match = False
                if match:
                    self.Win(color)
                    return


    #Check if player win after his move
    def checkWinner(self, color):
        self.checkRow(color)
        self.checkCol(color)
        self.checkDiagDownRight(color)
        self.checkDiagUpRight(color)

        #If board is full of pawns and no-one win then send that is draw
        if self.checkdraw():
            self.gameDraw()

    def checkdraw(self):
        return self.move >= 19*19

    def gameDraw(self):
        self.gameOver = True
        return self.gameOver

    def Win(self, color):
        self.gameOver = True
        self.winner = color
        return self.gameOver

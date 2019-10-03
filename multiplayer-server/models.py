import uuid

class ValidationFailed:
    def __init__(self):
        self.body = "Validation Failed"
        self.status_code = 401

class Game():
    def __init__(self):
        board = []
        '''Add each board row here'''
        for x in range(0,19):
            board.append(['','','','','','','','','','','','','','','','','','',''])

        self.board = board
        self.move = 0
        self.whiteID = None
        self.blackID = None
        self.winner = None
        self.gameOver = False
        self.currentPlayer = ''


    def makeMove(self, x, y, color):
        '''Get the row at pos x'''
        if self.board[x][y] == '':
            self.board[x][y] = color
            self.move = self.move + 1
        else:
            raise ValidationFailed

    def switchPlayer(self, color):
        #Change the current player after turn
        if color == 'white':
            self.currentPlayer = 'black'
        else:
            self.currentPlayer = 'white'


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

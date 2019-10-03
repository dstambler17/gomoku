from flask import Flask
from flask_socketio import SocketIO, send, emit
from models import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
game = None;

'''For when a player joins the game'''
@socketio.on('addNewPlayer')
def handleMessage(data):
    global game
    if game is None:
        game = Game()
        wid = str(uuid.uuid4())
        if '=' in wid:
            wid = wid.replace('=', '')
        game.whiteID = wid
        game.currentPlayer = 'white'
        emit('addNewPlayer',{'color' : 'white', 'id' : game.whiteID, 'moves' : game.move, 'gameBoard' : game.board, 'code' : '201'})
    elif game is not None and game.blackID is None:
        bid = str(uuid.uuid4())
        if '=' in bid:
            bid = bid.replace('=', '')
        #game.blackID = str(uuid.uuid4())
        game.blackID = bid
        emit('addNewPlayer',{'color' : 'black', 'id' : game.blackID, 'moves' : game.move, 'gameBoard' : game.board, 'code' : '201'})
    else:
        print(game.whiteID)
        print(game.blackID)
        emit('addNewPlayer', {'err': 'Game is occupied', 'code' : '401'})


'''For when a player makes a move'''
@socketio.on('message')
def handleMessage(data):
    if game is None:
        emit('errorMove', {'error' : 'The game does not exist anymore'})
        return
    #Check if the board has a winner and return winner
    if game.gameOver:
        print("winner issue")
        emit('errorMove', {'error' : 'The game is over'})
        return

    rbid = data['id']
    if '=' in data['id']:
        rbid = requestBody['id'].replace('=', '')
    if rbid != game.whiteID and rbid != game.blackID:
        print('bad id')
        emit('errorMove', {'error' : 'Invalid Id'})
        return

    color = data['color']
    '''check if the right client is playing, if not send error'''
    if color != game.currentPlayer:
        print('no turn')
        emit('errorMove', {'error' : 'Not your turn'})
        return

    '''Add the move to the game board'''
    x = int(data['x'])
    y = int(data['y'])
    try:
        game.makeMove(x, y, color)
    except (ValidationFailed) as e:
        emit('errorMove', {'error' : 'Cannot make move'})
        return

    game.checkWinner(color)
    game.switchPlayer(color)

    winner = game.winner
    if game.winner is None:
        winner = ''
    else:
        print("WINNER")
        print(game.winner)

    send({'color': color, 'your_row': x, 'your_col' : y, 'winner': winner, 'gameover' : game.gameOver}, broadcast=True)
    print(data['color'])

if __name__ == '__main__':
	socketio.run(app)

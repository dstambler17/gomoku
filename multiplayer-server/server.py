from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from models import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
games = []
player_count = 0


'''For when a player joins the game'''
@socketio.on('addNewPlayer')
def handleMessage(data):
    global games
    global player_count
    if player_count%2 == 0:
        game = Game()
        new_roomId = str(uuid.uuid4())
        if '=' in new_roomId:
            new_roomId = new_roomId.replace('=', '')
        game.roomID = new_roomId
        wid = str(uuid.uuid4())
        if '=' in wid:
            wid = wid.replace('=', '')
        game.whiteID = wid
        game.currentPlayer = 'white'
        games.append(game)
        join_room(game.roomID)
        player_count = player_count + 1
        emit('addNewPlayer',{'color' : 'white', 'id' : game.whiteID, 'moves' : game.move, 'gameBoard' : game.board, 'code' : '201', 'room' : game.roomID})
    else: #add black to game
        game = games[-1]
        bid = str(uuid.uuid4())
        if '=' in bid:
            bid = bid.replace('=', '')
        #game.blackID = str(uuid.uuid4())
        game.blackID = bid
        join_room(game.roomID)
        player_count = player_count + 1
        emit('addNewPlayer',{'color' : 'black', 'id' : game.blackID, 'moves' : game.move, 'gameBoard' : game.board, 'code' : '201', 'room' : game.roomID})
    '''else:
        print(game.whiteID)
        print(game.blackID)
        emit('addNewPlayer', {'err': 'Game is occupied', 'code' : '401'})'''

'''For when a player reloads their current game'''
@socketio.on('loadPlayer')
def handleMessage(data):
    global games
    roomId = data['room']
    playerId = data['player']
    game = None
    if '=' in roomId:
        roomId = roomId.replace('=', '')
    for g in games:
        if g.roomID == roomId:
            game = g
    if game is None:
        emit('errorMove', {'error' : 'The game does not exist anymore'})
        return
    color = ''
    if playerId == game.blackID:
        color = 'black'
    elif playerId == game.whiteID:
        color = 'white'
    else:
        emit('errorMove', {'error' : 'The game does not exist anymore'})
        return
    join_room(roomId)
    emit('loadPlayer',{'color' : color, 'id' : playerId, 'moves' : game.move, 'gameBoard' : game.board, 'code' : '201', 'room' : game.roomID})

'''For when a player starts a new game'''
@socketio.on('leaveGame')
def handleMessage(data):
    print("YOO")
    global games
    global player_count
    roomId = data['roomID']
    game = None
    if '=' in roomId:
        roomId = roomId.replace('=', '')
    for g in games:
        if g.roomID == roomId:
            game = g
    if game is None:
        emit('errorMove', {'error' : 'The game does not exist anymore'})
        return
    if game.blackID is None:
        player_count = player_count - 1
    else:
        player_count = player_count - 2
    if player_count < 0:
        player_count = 0
    games.remove(game)
    emit('leaveGame', {'playerId' : data['playerId']}, room=roomId)
    leave_room(roomId)


'''For when a player makes a move'''
@socketio.on('message')
def handleMessage(data):
    global games
    game = None
    roomId = data['roomID']
    if '=' in roomId:
        roomId = roomId.replace('=', '')
    for g in games:
        if g.roomID == roomId:
            game = g

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

    send({'color': color, 'your_row': x, 'your_col' : y, 'winner': winner, 'gameover' : game.gameOver}, room=game.roomID)
    print(data['color'])

if __name__ == '__main__':
	socketio.run(app)

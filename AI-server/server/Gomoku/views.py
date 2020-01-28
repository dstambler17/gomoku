import sys
import json
import uuid
from flask import Blueprint, request, jsonify
from server.models import Game
from server import mongo
from server.errorHandler.errors import *
#games = [];
Gomoku = Blueprint('Gomoku', __name__)


@Gomoku.route('/newGame', methods=['POST'])
def setup_match():
    #get games from mongodb
    games = mongo.db.AISinglePlayer
    game = Game()
    #Interesting safari test situation
    if '=' in game.gameID:
        game.gameID = game.gameID.replace('=', '')
    game.playerColor = 'white' #means black is AI color

    dictGame = game.__dict__
    print(dictGame)
    games.insert(dictGame)
    return jsonify({'color' : game.playerColor, 'id' : game.gameID}), 201

'''Load Game'''
@Gomoku.route('/getGame/<id>', methods=['GET'])
def load_match(id):

    if '=' in id:
        id = id.replace('=', '')
    game = None
    #query mongodb for games
    games = mongo.db.AISinglePlayer
    game = games.find_one({'gameID' : id})
    if not game:
        return jsonify({'err_msg': 'No game found'}), 404

    return jsonify({'color': game['playerColor'], 'gameBoard' : game['board'], 'moves' : game['move']})

@Gomoku.route('/playMove', methods=['POST'])
def playMove():

    '''contain:, x, y, id'''
    requestBody = json.loads(request.get_data())
    print(requestBody)

    '''START OF VALIDITY CHECKS'''
    game = None
    rbid = requestBody['id']
    #Safari issue fix
    if '=' in requestBody['id']:
        rbid = requestBody['id'].replace('=', '')
    #get data from mongodb
    games = mongo.db.AISinglePlayer
    gameDict = games.find_one({'gameID' : rbid})
    game = Game(gameDict)
    if not gameDict:
        return jsonify({'err_msg': 'No game found'}), 404
    #Check if the board has a winner and return winner
    if game.gameOver:
        return jsonify({'err_msg': 'The game is over!'}), 401
    '''END OF VALIDITY CHECKS '''


    '''Add the move to the game board'''
    x = int(requestBody['x'])
    y = int(requestBody['y'])
    try:
        game.makeMove(x, y)
    except (ValidationFailed) as e:
        jsonify(e.body), e.status_code

    game.checkWinner('white')
    comp_row, comp_col = game.makeAIMove(x, y)
    #game.checkWinner('black')

    winner = game.winner
    if game.winner is None:
        winner = ''

    #update the data in mongodb
    gameDictRes = game.__dict__
    myquery = {'gameID': rbid }
    newvalues = { "$set": gameDictRes }
    games.update_one(myquery, newvalues)
    print(game.gameOver)
    return jsonify({'Computer_Move_Row': comp_row, 'Computer_Move_Col' : comp_col, 'Winner': winner, 'GameOver' : game.gameOver}), 201

@Gomoku.route('/deleteGame/<id>', methods=['DELETE'])
def deleteGame(id):
    #global games
    games = mongo.db.AISinglePlayer
    game = games.find_one({'gameID' : id})
    if not game:
        return jsonify({'err_msg': 'No game found'}), 404
    game = games.delete_one({'gameID' : id})

    return jsonify({}), 204


@Gomoku.route('/testAI', methods=['GET'])
def testAI():
    game_test = Game()
    game_test.playerColor = 'white'
    board_test = []
    for x in range(0,19):
            board_test.append([''] * 19)
    
    game_test.board = board_test
    board_test[0][0] = 'white'
    board_test[16][17] = 'black'
    board_test[15][18] = 'black'
    board_test[18][1] = 'black'
    board_test[18][2] = 'black'

    
    game_test.board = board_test
    
    
    comp_row, comp_col = game_test.makeAIMove(5, 6)
    print(board_test)
    return jsonify({'comp_row' : comp_row, 'comp_col' : comp_col}), 200

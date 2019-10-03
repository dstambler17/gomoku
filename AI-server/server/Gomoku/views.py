import sys
import json
import uuid
from flask import Blueprint, request, jsonify
from server.models import Game
from server.errorHandler.errors import *
games = [];
Gomoku = Blueprint('Gomoku', __name__)


@Gomoku.route('/newGame', methods=['POST'])
def setup_match():
    global games
    game = Game()
    #Interesting safari test situation
    if '=' in game.gameID:
        game.gameID = game.gameID.replace('=', '')
    game.playerColor = 'white' #means black is AI color
    games.append(game)
    return jsonify({'color' : game.playerColor, 'id' : game.gameID}), 201

'''Load Game'''
@Gomoku.route('/getGame/<id>', methods=['GET'])
def load_match(id):
    global games
    if '=' in id:
        id = id.replace('=', '')
    game = None
    for g in games:
        if g.gameID == id:
            game = g
    if game is None:
        return jsonify({'err_msg': 'No game found'}), 404

    return jsonify({'color': game.playerColor, 'gameBoard' : game.board, 'moves' : game.move})

@Gomoku.route('/playMove', methods=['POST'])
def playMove():

    global games
    '''contain:, x, y, id'''
    requestBody = json.loads(request.get_data())
    print(requestBody)

    '''START OF VALIDITY CHECKS'''
    game = None
    rbid = requestBody['id']
    #Safari issue fix
    if '=' in requestBody['id']:
        rbid = requestBody['id'].replace('=', '')
    for g in games:
        print(g.gameID)
        if g.gameID == rbid:
            game = g
    if game is None:
        return jsonify({'err_msg': 'No game found'}), 404
    #Check if the board has a winner and return winner
    if game.gameOver:
        print("winner issue")
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

    return jsonify({'Computer_Move_Row': comp_row, 'Computer_Move_Col' : comp_col, 'Winner': winner, 'GameOver' : game.gameOver}), 201

@Gomoku.route('/deleteGame/<id>', methods=['DELETE'])
def deleteGame(id):
    global games
    for g in games:
        if g.gameID == id:
            game = g
    if game is None:
        return jsonify({'err_msg': 'No game found'}), 404
    games.remove(game)
    return jsonify({}), 204

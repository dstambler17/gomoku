import Game from './Game.js';

$(document).ready(function() {
    var socket = io.connect('http://localhost:5000/');
    console.log("Hello")
    const game = new Game(socket)

    game.createGameBoard()
    console.log(game.getMoves())
    /*$('#sendbutton').on('click', function() {
        socket.send($('#myMessage').val());
        $('#myMessage').val('');
    });*/
});
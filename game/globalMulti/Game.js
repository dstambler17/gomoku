class Game {
    //add 'socket' as one of the parameters
    constructor(socket) {
      this.board = [];
      this.color = '';
      this.moves = 0;
      this.winner = '';
      this.gameOver = false
      this.playerId = ''
      this.socket = socket
    }


    getMoves(){
        return this.moves;
    }
            tileClickHandler(e) {
                console.log(e.target.id)
                //Get row from tile id
                    let row;
                    if(e.target.id.split('_')[1][1] != undefined){
                        row = e.target.id.split('_')[1][0] + e.target.id.split('_')[1][1];
                    }else
                    {
                        row = e.target.id.split('_')[1][0];
                    }

                //Get column from tile id
                    let col;
                    if(e.target.id.split('_')[2][1] != undefined){
                        col = e.target.id.split('_')[2][0] + e.target.id.split('_')[2][1];
                    }else{
                        col = e.target.id.split('_')[2][0];
                    }

                console.log(row)
                console.log(col)

                const coordinates = '(' + row.toString() + ',' + col.toString() + ')'


                this.updateBoard(this.getColor(), row, col, e.target.id);
            }

        //Create the Game board and attach click event to tiles
        createGameBoard() {
            //First load the board
             this.createTiles();
            //Then either create/join a game on the server side or load
            var that = this;
            that.socket.on('addNewPlayer', function(data) {
                    console.log(data);
                    if (data['code'] === '201'){
                        that.color = data['color']
                        that.moves = data['moves']
                        document.getElementById("turn-num").innerText = that.moves;
                        $('#color').css("background-color", `${that.color}`);
       
                        document.cookie = 'userid:' + data['id']
                        that.playerId = data['id']

                        if (data['color'] == 'black'){
                            that.loadPieces(data['gameBoard'])
                        }
                    }
                    else{
                        alert('game is full!')
                    }
            });
            this.socket.on('message', function(data) {
                console.log('Received message');
                //Don't play anymore if winner
                if (that.gameOver){
                    return
                }
                $(".center").prop(`disabled`, true);
                if(color !== that.getColor()){
                    $(".center").prop(`disabled`, false);
                }
                //Make move for the player
                
                //$('#color').css("background-color", `${this.getColor()}`);
                const move_row = data['your_row']
                const move_col = data['your_col']
                const move_id = 'button_' + move_row.toString() + '_' + move_col.toString()
                const move_color = data['color']
        
                $(`#${move_id}`).css("backgroundImage", `url(images/${move_color}Piece.png)`).prop('disabled', true);
                that.board[move_row][move_col] = move_color[0];
                that.moves++;
                document.getElementById("turn-num").innerText = that.moves;
                that.handleWin(data['gameover'] ,data['winner'])
            });
        
            this.socket.on('errorMove', function(data) {
                alert(data['error'])
            })
        }

          loadPieces(board){
            console.log(board)
            var that = this
            $('.center').children('button').each(function () {
                console.log('hi')
                let elemIdArr = (this.id).toString().split('_')
                 const row = parseInt(elemIdArr[1])
                 const col = parseInt(elemIdArr[2])
                 console.log(row)
                 console.log(col)
                 let color;
                 if (board[row][col] === 'white'){
                   color = 'white'
                   $(`#${this.id}`).css("backgroundImage", `url(images/${color}Piece.png)`).prop('disabled', true);
                   that.board[row][col] = color[0];
                 }
                 else if (board[row][col] === 'black'){
                   color = 'black'
                   $(`#${this.id}`).css("backgroundImage", `url(images/${color}Piece.png)`).prop('disabled', true);
                   that.board[row][col] = color[0];
                 }
            });

          }

          //Create tiles for game board
          createTiles(){
            //Create tiles in the DOM
            this.socket.emit('addNewPlayer', {})
            for (let i = 0; i < 19; i++) {
              for (let j = 0; j < 18; j++) {
                $('.center').append(`<button class="tile" id="button_${i}_${j}"></button>`)
              }
              $('.center').append(`<button class="tile" id="button_${i}_18" style="float:none;"/>`);
            }

            //Attach click listener to tiles
            for (let i = 0; i < 19; i++) {
              this.board.push(['']);
              for (let j = 0; j < 19; j++) {
                $(`#button_${i}_${j}`).on('click', this.tileClickHandler.bind(this));
              }
            }

            //Attach the event listener to the new game button
            //$('#new_button').on('click', this.startNewGame.bind(this));
          }

        //get current player
        getColor(){
            return this.color
        }

        //get AI color
        getOppositeColor(){
            if (this.color = 'white') {
                return 'black'
            } else{
                return 'white'
            }
        }

      //Update board
      updateBoard(color, row, col) {
        //make a request to update the board
        var that = this
        console.log("COLOR")
        console.log(this.color)
        const cookieId = this.playerId
        const data = {"x" : row.toString(), "y" : col.toString(), "id" : cookieId, 'color' : color}
        this.socket.send(data)
      }

      handleWin(game_is_over, gameWinner){
        if (!game_is_over){
            return
        } else if (game_is_over && gameWinner === ''){
            alert('Tie!')
            this.gameOver = true
        } else {
            let winner = document.getElementById('winner')
            $('#color').css("margin-bottom", "5px");
            winner.style.display = 'block'
            winner.style.fontSize = '20px'
            winner.style.marginBottom = '1em'
            winner.innerText = 'Winner: ' + gameWinner.toUpperCase()
            this.gameOver = true
        }
      }


}

export default Game
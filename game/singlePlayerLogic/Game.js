class Game {
    //add 'socket' as one of the parameters
    constructor() {
      this.board = [];
      this.color = '';
      this.moves = 0;
      this.winner = '';
      this.gameOver = false
    }

    startNewGame(){
        const cookieId = (document.cookie).split('userid:')[1]
        $.ajax({
            type: "DELETE",
            url: ' http://127.0.0.1:5000/gomoku/deleteGame/' + cookieId,
            data: {},
            success:
             function( data, textStatus, jQxhr ){
                document.cookie = ''
                location.reload()
             },
            error:
            function( jqXhr, textStatus, errorThrown ){
               alert('Invalid Game ID')
            }
          });
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
          if ((document.cookie).includes("userid:")){
            //Continue existing game
            const cookieId = (document.cookie).split('userid:')[1]
            console.log(cookieId)
            $.ajax({
             type: "GET",
             url: ' http://127.0.0.1:5000/gomoku/getGame/' + cookieId,
             data: {},
             success:
              function( data, textStatus, jQxhr ){
                  console.log(data)
                  that.color = data['color']
                  that.moves = data['moves']
                  document.getElementById("turn-num").innerText = that.moves;
                  $('#color').css("background-color", `${that.color}`);
                  that.loadPieces(data['gameBoard'])
                  that.color = data['color']
              },
             error:
             function( jqXhr, textStatus, errorThrown ){
                alert('Invalid Game ID')
                console.log( errorThrown );
             }
           });

          } else {
            //Join a new game
              $.ajax({
               type: "POST",
               url: ' http://127.0.0.1:5000/gomoku/newGame',
               data: {},
               success:
                function( data, textStatus, jQxhr ){
                    console.log(data)
                    document.cookie = 'userid:' + data['id']
                    that.color=data['color']
                    console.log(this.color)
                    $('#color').css("background-color", `${that.color}`);
                    if (data['color'] == 'black'){
                      that.loadPieces(data['gameBoard'])
                    }
                },
               error:
               function( jqXhr, textStatus, errorThrown ){
                  alert('This game cannot accept any more players')
                  console.log( errorThrown );
               }
             });
           }
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
            $('#new_button').on('click', this.startNewGame.bind(this));
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
      updateBoard(color, row, col, tile) {
        //make a request to update the board
        var that = this
        console.log("COLOR")
        console.log(this.color)
        const cookieId = (document.cookie).split('userid:')[1]
        const data = {"x" : row.toString(), "y" : col.toString(), "id" : cookieId}
        $.ajax({
         type: "POST",
         url: ' http://127.0.0.1:5000/gomoku/playMove',
         data: JSON.stringify(data),
         success:
            function( data, textStatus, jQxhr ){
              //Don't play anymore if winner
              if (that.gameOver){
                return
              }
              $(".center").prop(`disabled`, true);
              if(color !== that.getColor()){
                $(".center").prop(`disabled`, false);
              }
              //Make move for the player
              $(`#${tile}`).css("backgroundImage", `url(images/${color}Piece.png)`).prop('disabled', true);
              that.board[row][col] = color[0];
              
              //$('#color').css("background-color", `${this.getColor()}`);
              const computer_move_row = data['Computer_Move_Row']
              const computer_move_col = data['Computer_Move_Col']
              const computer_move_id = 'button_' + computer_move_row.toString() + '_' + computer_move_col.toString()
              const oppositeColor = that.getOppositeColor()
              setTimeout(function () {
                    //Make comp move
                    $(`#${computer_move_id}`).css("backgroundImage", `url(images/${oppositeColor}Piece.png)`).prop('disabled', true);
                    that.board[computer_move_row][computer_move_col] = oppositeColor[0];
                    that.moves++;
                    document.getElementById("turn-num").innerText = that.moves;
                    that.handleWin(data['GameOver'] ,data['Winner'])
                }, 1000);    
            },
         error:
           function( jqXhr, textStatus, errorThrown ){
              console.log( errorThrown );
           }
        });
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
class Game {
    constructor() {
      //array for savings movements of players
      this.board = [];
      //count of moves
      this.moves = 0;
      this.gameOver = false;
    }

    getMoves(){
        return this.moves;
    }
            tileClickHandler(e) {
                //No moves can be made once the game is over
                if (this.gameOver){
                    return
                }

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

                //get color

                //If is not your turn
                /*if (!player.getCurrentTurn() || !game) {
                alert('Its not your turn!');
                return;
                }

                //If tile has been already played
                else{
                if ($(this).prop('disabled')) {
                    alert('This tile has already been played on!');
                    return;
                }

                //Update board after player turn.
                //game.playTurn(this); */
                this.updateBoard(this.getColor(), row, col, e.target.id);

                
                this.checkWinner(row, col);

                this.updateTurn();


            }

        //Create the Game board and attach click event to tiles
        createGameBoard() {
            $('#color').css("background-color", `${this.getColor()}`);
            this.createTiles();
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
          }

        //get current player
        getColor(){
            const color = (this.moves%2 === 0) ? 'white' : 'black';
            return color;
        }

      //Update board
      updateBoard(color, row, col, tile) {
        $(".center").prop(`disabled`, true);
        if(color !== this.getColor()){
          $(".center").prop(`disabled`, false);
        }
        $(`#${tile}`).css("backgroundImage", `url(images/${color}Piece.png)`).prop('disabled', true);
        this.board[row][col] = color[0];
      }

      //increment the turn counter
      updateTurn(){
        if (this.gameOver) {
            return;
        }
        this.moves++;
        $('#color').css("background-color", `${this.getColor()}`);
        document.getElementById("turn-num").innerText = this.moves;
      }

      //HandleTheWinner
      handleWinner(){
          const color = this.getColor()
          let winner = document.getElementById('winner')
          $('#color').css("margin-bottom", "5px");
          winner.style.display = 'block'
          winner.style.fontSize = '20px'
          winner.style.marginBottom = '1em'
          winner.innerText = 'Winner: ' + color.toUpperCase()
          this.gameOver = true
      }


      //Methods for checking the winner
      checkWinner(row, col){
          console.log(this.board)
          const horizCheck = this.checkHorizontal(row)
          const vertCheck = this.checkVertical(col)
          const negdiagonalCheck = this.checkDiagonal_neg_slope(row, col)
          const posdiagonalCheck = this.checkDiagonal_pos_slope(row, col)

          if (horizCheck || vertCheck || negdiagonalCheck || posdiagonalCheck){
            this.handleWinner()
          }

          //checkTie
          if (this.moves >= 360){
            alert('Congrats, you both tied!!!')
            this.gameOver = true            
          }
      }

      checkHorizontal(row){
        let count = 0;
        const player = (this.getColor() == 'white') ? 'w' : 'b'
        for(var i= 0; i < 19; i++){
            if (this.board[row][i] == player){
                count++;
            } else{
                count = 0;
            }

            if (count == 5){
                return true
            }
        }
        return false
      }

      checkVertical(col){
        let count = 0;
        const player = (this.getColor() == 'white') ? 'w' : 'b'
        for(var i= 0; i < 19; i++){
            if (this.board[i][col] == player){
                count++;
            } else{
                count = 0;
            }

            if (count == 5){
                return true
            }
        }
        return false
      }

      checkDiagonal_neg_slope(row, col){
        let x = row
        let y = col
        const player = (this.getColor() == 'white') ? 'w' : 'b'
        //roll back to start of the diagonal
        while (x> 0 && y> 0){
            x--
            y--
        }
        let count = 0
        while (x<= 18 && y<=18){
            if (this.board[x][y] == player){
                count++;
            } else{
                count = 0;
            }

            if (count == 5){
                return true
            }
            x++
            y++
        }

        return false
      }

      checkDiagonal_pos_slope(row, col){
        let x = row
        let y = col
        const player = (this.getColor() == 'white') ? 'w' : 'b'
        //roll back to start of the diagonal
        while (x> 0 && y> 0 && x < 18 && y<18){
            x++
            y--
        }
  
        let count = 0
        while (x<= 18 && y<=18 && x>= 0 && y>= 0){
            if (this.board[x][y] == player){
                count++;
            } else{
                count = 0;
            }

            if (count == 5){
                return true
            }
            x--
            y++
        }

        return false
      }



}

export default Game

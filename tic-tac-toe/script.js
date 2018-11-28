/*
 * Tic Tac Toe
 *
 * A Tic Tac Toe game in HTML/JavaScript/CSS.
 *
 * @author: Vasanth Krishnamoorthy
 */
var N_SIZE = 3,
  EMPTY = "&nbsp;",
  boxes = [],
  aiTurn = 'O',
  turn,
  score,
  moves;

// based on https://codepen.io/vasanthkay/pen/KVzYzG

/*
 * Initializes the Tic Tac Toe board and starts the game.
 */
function init() {
  var board = document.createElement('table');
  board.setAttribute("border", 1);
  board.setAttribute("cellspacing", 0);

  var identifier = 1;
  for (var i = 0; i < N_SIZE; i++) {
    var row = document.createElement('tr');
    board.appendChild(row);
    for (var j = 0; j < N_SIZE; j++) {
      var cell = document.createElement('td');
      cell.setAttribute('height', 120);
      cell.setAttribute('width', 120);
      cell.setAttribute('align', 'center');
      cell.setAttribute('valign', 'center');
      cell.classList.add('col' + j, 'row' + i);
      if (i == j) {
        cell.classList.add('diagonal0');
      }
      if (j == N_SIZE - i - 1) {
        cell.classList.add('diagonal1');
      }
      cell.identifier = identifier;
      cell.addEventListener("click", set);
      row.appendChild(cell);
      boxes.push(cell);
      identifier += identifier;
    }
  }

  document.getElementById("tictactoe").appendChild(board);
  choosePlayer();
}

function beginX() { 
  turn = "X";
  document.getElementById("tictactoe").style.display = 'block';
  document.getElementById("choose").style.display = 'none';
  startNewGame();
}


function secondO() {
  turn = "O";
  document.getElementById("tictactoe").style.display = 'block';
  document.getElementById("choose").style.display = 'none';
  startNewGame();
}

/*
 * New game
 */
function startNewGame() {
  score = {
    "X": 0,
    "O": 0
  };
  moves = 0;
  boxes.forEach(function (square) {
    square.innerHTML = EMPTY;
  });
  if (turn == aiTurn) {
    play()
  }
}

function choosePlayer() {
  document.getElementById("tictactoe").style.display = 'none';
  document.getElementById("choose").style.display = 'block';
}

/*
 * Check if a win or not
 */
function win(clicked) {
  // Get all cell classes
  var memberOf = clicked.className.split(/\s+/);
  for (var i = 0; i < memberOf.length; i++) {
    var testClass = '.' + memberOf[ i ];
    var items = contains('#tictactoe ' + testClass, turn);
    // winning condition: turn == N_SIZE
    if (items.length == N_SIZE) {
      return true;
    }
  }
  return false;
}

function contains(selector, text) {
  var elements = document.querySelectorAll(selector);
  return [].filter.call(elements, function (element) {
    return RegExp(text).test(element.textContent);
  });
}

function allUnclickable() {
  boxes.forEach(function (square) {
    square.removeEventListener("click", set);
  });
}

function  allClickable() {
  boxes.forEach(function (square) {
    square.addEventListener("click", set);
  });
}

/*
 * Sets clicked square and also updates the turn.
 */
function set() {
  if (this.innerHTML !== EMPTY) {
    return;
  }
  allUnclickable();
  this.innerHTML = turn;
  moves += 1;
  score[ turn ] += this.identifier;
  if (win(this)) {
    setTimeout(function () {
        alert('Winner: Player ' + turn);
        choosePlayer();
    }, 30);
    
  } else if (moves === N_SIZE * N_SIZE) {
    setTimeout(function () {
      alert("Draw");
      choosePlayer();
    }, 30);
  } else {
    turn = turn === "X" ? "O" : "X";

    document.getElementById('turn').textContent = 'Player ' + turn + ' turn';
    if (turn == aiTurn) {
      play()
    }
    allClickable();
  }
}

function play() {
  for (let i = 0; i < boxes.length; i++) {
    const square = boxes[i];
    if (square.innerHTML == EMPTY) {
      set.call(square);
      // square.innerHTML = turn;
      // turn = turn === "X" ? "O" : "X";
      break;
    }
  }
}


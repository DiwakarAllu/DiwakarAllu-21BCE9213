const socket = io();

let gameState = null;
let selectedCharacter = null;

socket.on("init", (data) => {
  gameState = data;
  renderGameState();
});

socket.on("update", (data) => {
  gameState = data;
  renderGameState();
});

socket.on("invalid_move", () => {
  document.getElementById("message").innerText = "Invalid move. Try again.";
});

function renderGameState() {
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  gameState.grid.forEach((row) => {
    row.forEach((cell) => {
      const div = document.createElement("div");
      div.className = "cell";
      div.innerText = cell;
      if (cell.startsWith(gameState.currentPlayer) && !gameState.winner) {
        div.onclick = () => selectCharacter(cell);
      }
      grid.appendChild(div);
    });
  });
  document.getElementById("current-player").innerText = gameState.winner
    ? `Winner: ${gameState.winner}`
    : `Current Player: ${gameState.currentPlayer}`;
  document.getElementById("current-player").style.color = gameState.winner
    ? "green"
    : "black";
  document.getElementById("selected-character").innerText = `Selected: ${
    selectedCharacter || "None"
  }`;
  document.getElementById("message").innerText = "";
  renderMoveHistory();
  hideAllButtons();
}

function renderMoveHistory() {
  const movesLog = document.getElementById("moves-log");
  movesLog.innerHTML = gameState.moveHistory.join("<br>");
}

function selectCharacter(character) {
  selectedCharacter = character;
  document.getElementById(
    "selected-character"
  ).innerText = `Selected: ${selectedCharacter}`;
  showButtonsForCharacter(character);
}

function move(direction) {
  if (!selectedCharacter) return;
  socket.emit("move", {
    move: {
      player: gameState.currentPlayer,
      character: selectedCharacter,
      direction,
    },
  });
  selectedCharacter = null;
  hideAllButtons();
}

function startOver() {
  socket.emit("start_over");
}

function hideAllButtons() {
  document
    .querySelectorAll(".control-button")
    .forEach((button) => (button.style.display = "none"));
}

function showButtonsForCharacter(character) {
  hideAllButtons();
  if (
    character.endsWith("P1") ||
    character.endsWith("P2") ||
    character.endsWith("P3") ||
    character.endsWith("H1")
  ) {
    document.getElementById("L").style.display = "inline-block";
    document.getElementById("R").style.display = "inline-block";
    document.getElementById("F").style.display = "inline-block";
    document.getElementById("B").style.display = "inline-block";
  } else if (character.endsWith("H2")) {
    document.getElementById("FL").style.display = "inline-block";
    document.getElementById("FR").style.display = "inline-block";
    document.getElementById("BL").style.display = "inline-block";
    document.getElementById("BR").style.display = "inline-block";
  }
}

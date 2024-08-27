from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Initial game state
initial_game_state = {
    "currentPlayer": "A",
    "grid": [
        ["A-P1", "A-P2", "A-H1", "A-H2", "A-P3"],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["B-P1", "B-P2", "B-H1", "B-H2", "B-P3"]
    ],
    "moveHistory": [],
    "winner": None
}

game_state = initial_game_state.copy()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('init', game_state)

@socketio.on('move')
def handle_move(data):
    print(f"Received move: {data['move']}")
    if process_move(data['move']):
        check_winner()
        emit('update', game_state, broadcast=True)
    else:
        emit('invalid_move', broadcast=True)

@socketio.on('start_over')
def handle_start_over():
    global game_state
    game_state = {
        "currentPlayer": "A",
        "grid": [
            ["A-P1", "A-P2", "A-H1", "A-H2", "A-P3"],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["B-P1", "B-P2", "B-H1", "B-H2", "B-P3"]
        ],
        "moveHistory": []
    }
    emit('init', game_state, broadcast=True)


def process_move(move):
    player = move["player"]
    character = move["character"]
    direction = move["direction"]

    # Find the character's current position
    current_row, current_col = None, None
    for row in range(5):
        for col in range(5):
            if game_state["grid"][row][col] == character:
                current_row, current_col = row, col
                break

    if current_row is None or current_col is None:
        print("Character not found on the grid.")
        return False

    # Calculate new position based on direction
    if character.endswith("P1") or character.endswith("P2") or character.endswith("P3"):  # Pawn
        new_row, new_col = move_pawn(current_row, current_col, direction, player)
    elif character.endswith("H1"):  # Hero1
        new_row, new_col = move_hero1(current_row, current_col, direction, player)
    elif character.endswith("H2"):  # Hero2
        new_row, new_col = move_hero2(current_row, current_col, direction, player)

    print(f"Moving {character} from ({current_row}, {current_col}) to ({new_row}, {new_col})")

    # Validate and update the game state
    if is_valid_move(new_row, new_col, player):
        captured_character = game_state["grid"][new_row][new_col]
        game_state["grid"][current_row][current_col] = ""
        game_state["grid"][new_row][new_col] = character
        game_state["currentPlayer"] = "B" if player == "A" else "A"
        
        if captured_character:
            game_state["moveHistory"].append(f"{character}:{direction} (Captured {captured_character})")
        else:
            game_state["moveHistory"].append(f"{character}:{direction}")
        
        return True
    else:
        print("Invalid move.")
        return False

def move_pawn(row, col, direction, player):
    if direction == "L":
        col = max(0, col - 1)
    elif direction == "R":
        col = min(4, col + 1)
    elif direction == "F":
        row = row + 1 if player == "A" else row - 1
    elif direction == "B":
        row = row - 1 if player == "A" else row + 1
    return row, col

def move_hero1(row, col, direction, player):
    if direction == "L":
        col = max(0, col - 2)
    elif direction == "R":
        col = min(4, col + 2)
    elif direction == "F":
        row = row + 2 if player == "A" else row - 2
    elif direction == "B":
        row = row - 2 if player == "A" else row + 2
    return row, col

def move_hero2(row, col, direction, player):
    if direction == "FL":
        new_row = row + 2 if player == "A" else row - 2
        new_col = col - 2
    elif direction == "FR":
        new_row = row + 2 if player == "A" else row - 2
        new_col = col + 2
    elif direction == "BL":
        new_row = row - 2 if player == "A" else row + 2
        new_col = col - 2
    elif direction == "BR":
        new_row = row - 2 if player == "A" else row + 2
        new_col = col + 2
    else:
        return row, col
    if 0 <= new_row < 5 and 0 <= new_col < 5:
        return new_row, new_col
    else:
        return row, col

def is_valid_move(row, col, player):
    if row < 0 or row > 4 or col < 0 or col > 4:
        return False
    if game_state["grid"][row][col].startswith(player):
        return False
    return True

def check_winner():
    a_characters = sum(cell.startswith('A') for row in game_state["grid"] for cell in row)
    b_characters = sum(cell.startswith('B') for row in game_state["grid"] for cell in row)
    
    if a_characters == 0:
        game_state["winner"] = "Player B"
    elif b_characters == 0:
        game_state["winner"] = "Player A"

if __name__ == '__main__':
    socketio.run(app, debug=True)

# Turn-Based Chess-Like Game

## Overview
This project is a turn-based chess-like game implemented using Flask and Socket.IO for real-time communication. The game features two players, Player A and Player B, each controlling a set of characters on a 5x5 grid. The objective is to eliminate all of the opponent's characters to win the game.

## Features
- Real-time updates using websockets
- Turn-based gameplay
- Different movement rules for different characters
- Capture mechanics
- Game reset functionality
- Winner announcement

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/DiwakarAllu/DiwakarAllu-21BCE9213.git
    cd DiwakarAllu-21BCE9213
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the server:
    ```bash
    python app.py
    ```

4. Open your browser and navigate to `http://localhost:5000`.

## Usage
- **Start the Game**: Open the game in two different browser windows or tabs to simulate two players.
- **Select a Character**: Click on a character to select it.
- **Move the Character**: Use the buttons to move the selected character. The available buttons will change based on the character type.
- **Capture**: Move your character to a cell occupied by an opponent's character to capture it.
- **Win the Game**: Eliminate all of your opponent's characters to win the game. The winner will be announced in bold green text at the top of the screen.
- **Start Over**: Click the "Start Over" button to reset the game.

## Game Rules
- **Pawns (P1, P2, P3)**: Can move left (L), right (R), forward (F), or backward (B).
- **Hero1 (H1)**: Can move two cells left (L), right (R), forward (F), or backward (B).
- **Hero2 (H2)**: Can move two cells diagonally (FL, FR, BL, BR).

## File Structure
- `app.py`: The main server-side script that handles game logic and websocket communication.
- `templates/index.html`: The HTML template for the game interface.
- `static/js/script.js`: The client-side JavaScript for handling user interactions and websocket communication.
- `static/css/styles.css`: The CSS file for styling the game interface.

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements
- Flask: https://flask.palletsprojects.com/
- Socket.IO: https://socket.io/


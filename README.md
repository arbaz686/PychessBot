# PyChess


![Preview(speeded up)](https://user-images.githubusercontent.com/78041366/135681678-6a5f4634-0030-49b5-b230-b6c7cb6b7c7a.gif)

A chess Bot made in python with the help of PyGame. This chess bot uses Min-Max search algorithm with alpha beta pruning and iterative deepening to find the best move to play against its opponent.

It also uses a large data set of 1,8 0,000+ games played by GMs so that it can make the optimal opening moves.

The chess board supports moves like pawn-promotion, double pawn push, castling on king and queen side, and en passant from black's side.


## Installation

```
git clone https://github.com/DivyanshMittal-exe/PyChess.git

cd PyChess
pip install -r requirements.txt
```

## Usage

```
python -m ChessBoard
```

## Instructions:
- You play as white, while the bot plays as black
- Clicking on any white piece will show the possible legal moves and captures available.
- Selecting on any of the legal moves square will move the piece to the desired location
<hr>
<sup>During the initial phase, when a lot moves are possible, the bot might take some time to process (upto 10 sec) during which your move might not render yet</sup>


![Chess Board](Images/strt.png?raw=true "Start Menu")
![Chess Board](Images/SS.png?raw=true "Chess Board")

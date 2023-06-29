# BlackJack-Game

This repository contains a Python implementation of the popular card game, Blackjack. The game is designed to be played in the console and supports multiple players.

## Features

- The game supports up to 7 players.
- Each player starts with a default balance of 1000.
- Players can place bets ranging from 5 to 300.
- The game uses a standard deck of cards (2-10, J, Q, K, A).

## How to Play

1. The game starts by asking for the number of players.
2. Each player is then asked to enter their name.
3. For each round, players are asked if they want to play the round.
4. If a player chooses to play, they are asked to place their bet.
5. The game continues in this manner until the players choose to stop playing.

## Code Structure

The main function of the program is `jouer_partie()`, which is called at the bottom of the program and allows playing one or more games of blackjack.

The program uses global variables to store information about the players and the dealer. These are defined at the top of the program.

The constants are defined at the top of the program, they represent the parameters of the game. They are used in the functions of the program. You can modify them to change the game parameters (number of players, minimum bet, maximum bet, starting balance, etc.).

Some functions are recursive. We chose to use recursive functions to avoid repeating instructions in the program.

## Requirements

- Python 3.x

## Usage

To play the game, run the `main.py` script in your Python environment.

```bash
python main.py

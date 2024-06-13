"""
Tic Tac Toe

Using what you have learnt about Python programming, you will build a text-based version of the Tic Tac Toe game.
The game should be playable in the command line just like the Blackjack game we created on Day 11.
It should be a 2-player game, where one person is "X" and the other plays "O".

This is a simple demonstration of how the game works:

https://www.google.com/search?q=tic+tac+toe

You can choose how you want your game to look. The simplest is to create a game board using "|" and "_" symbols. But the design is up to you.
"""
from art import logo
import os


def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    print("    COLUMN")
    print("    1 2 3")
    labels = ["R", "O", "W"]
    for idx, row in enumerate(board, 1):
        print(f"{labels[idx-1]} {idx} {'|'.join(row)}")
        if idx < 3:
            print("   -------")
        else:
            print(" ")


def check_winner(board, player):
    # Check rows
    for row in board:
        if all(s == player for s in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_board_full(board):
    return all(all(cell != " " for cell in row) for row in board)


def get_move(player):
    while True:
        try:
            move = input(f"Player {player}, enter your move as a pair of integers from 1 to 3 with a space between (ROW COLUMN): ")
            row, col = map(int, move.split())
            row -= 1
            col -= 1
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid input. Row and column must be between 1 and 3.")
                continue
            return row, col
        except ValueError:
            print("Invalid input. Please enter integers (ROW COLUMN) from 1 to 3 separated by a space.")


def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    while True:
        print_board(board)
        row, col = get_move(players[current_player])

        if board[row][col] != " ":
            print("Invalid move. Try again.")
            continue
        board[row][col] = players[current_player]

        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} wins!")
            break

        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

        current_player = 1 - current_player


if __name__ == "__main__":
    tic_tac_toe()

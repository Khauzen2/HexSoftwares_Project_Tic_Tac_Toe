import tkinter as tk
import random
from tkinter import messagebox

# Global variables
board = [' ' for _ in range(9)]
current_player = 'X'
difficulty = 'Medium'  # Default difficulty

# Initialize the GUI
root = tk.Tk()
root.title("Tic-Tac-Toe Game")

# Game board buttons
buttons = []

# Check if someone has won
def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Check for draw
def check_draw(board):
    return all(space != ' ' for space in board)

# Handle player moves
def player_move(index):
    global current_player
    if board[index] == ' ' and current_player == 'X':
        board[index] = 'X'
        buttons[index].config(text='X')
        if check_winner(board, 'X'):
            messagebox.showinfo("Game Over", "Congratulations! You win!")
            reset_game()
        elif check_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
        else:
            current_player = 'O'
            computer_move()

# Easy mode: Random move
def easy_move():
    available_moves = [i for i, space in enumerate(board) if space == ' ']
    return random.choice(available_moves)

# Medium mode: Block if player is about to win
def medium_move():
    # Block the player's winning move if possible
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner(board, 'O'):
                board[i] = ' '
                return i
            board[i] = ' '
    # Otherwise, move randomly
    return easy_move()

# Hard mode: Attempt to win and block
def hard_move():
    # Try to win first
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner(board, 'O'):
                board[i] = ' '
                return i
            board[i] = ' '

    # Try to block the player
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_winner(board, 'X'):
                board[i] = ' '
                return i
            board[i] = ' '
    
    # Otherwise, move to the center if available
    if board[4] == ' ':
        return 4

    # Otherwise, move randomly
    return easy_move()

# Computer move logic
def computer_move():
    global current_player
    if difficulty == 'Easy':
        move = easy_move()
    elif difficulty == 'Medium':
        move = medium_move()
    else:  # Hard mode
        move = hard_move()

    board[move] = 'O'
    buttons[move].config(text='O')

    if check_winner(board, 'O'):
        messagebox.showinfo("Game Over", "Computer wins! Better luck next time.")
        reset_game()
    elif check_draw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_game()
    else:
        current_player = 'X'

# Reset the game
def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    for button in buttons:
        button.config(text=' ')

# Create the game board
for i in range(9):
    button = tk.Button(root, text=' ', font=('Arial', 20), width=5, height=2,
                       command=lambda i=i: player_move(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Menu for difficulty settings and two-player mode
menu = tk.Menu(root)
root.config(menu=menu)

# Difficulty submenu
difficulty_menu = tk.Menu(menu)
menu.add_cascade(label="Difficulty", menu=difficulty_menu)
difficulty_menu.add_command(label="Easy", command=lambda: set_difficulty('Easy'))
difficulty_menu.add_command(label="Medium", command=lambda: set_difficulty('Medium'))
difficulty_menu.add_command(label="Hard", command=lambda: set_difficulty('Hard'))

# Set difficulty
def set_difficulty(level):
    global difficulty
    difficulty = level
    messagebox.showinfo("Difficulty", f"Difficulty set to {level}.")

# Two-Player mode
def set_two_player():
    global current_player
    reset_game()
    current_player = 'X'
    messagebox.showinfo("Mode", "Two-Player mode activated!")

menu.add_command(label="Two-Player Mode", command=set_two_player)

# Run the GUI
root.mainloop()

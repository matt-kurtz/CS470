# Assignment 2 - 2-Player version
# Matthew Kurtz
# Dr. Soule - CS470 SU24

import os # Here I want to be able to clear the screen after each turn that the player takes

# For this assignment, I want to try to not be all over the place with my code. I'll try my best to add comments and explain everything I'm doing.
# First, let's create our Connect 4 board.
def create_board():
    # Since we already know what the size of the board should be, we can create a 6x7 board
    # Let's create two variables just in case we want to change the size in the future
    rows = 6
    cols = 7
    arr = [['.' for _ in range(cols)] for _ in range(rows)]
    return rows, cols, arr

# Here's a simple print function to make sure it's right
# We'll also add column numbers to make the choice easier for whoever is playing
def print_board(arr, cols):
    for row in arr:
        print(' '.join(row))
    print(''.join(['—' for _ in range((cols*2) - 1)]))
    print(' '.join([str(i) for i in range(cols)]))

# Now, let's create symbols for two players
# Player 1 wil have 0 and Player 2 will have X
# We'll need to get input from the user and then insert it appropriately into our board
def player_move(arr, rows, cols, p_num):
    # We'll have p_num as a parameter to know which character to use. For example '1' == player 1, '2' == player 2
    player = ' '
    if p_num == 1:
        player = '0'
    elif p_num == 2:
        player = 'X'
    
    # Now, let's get input for the column number from the player. We'll use the try/except keywords to make sure we get an integer.
    while True:
        try:
            x = int(input(f"Player {p_num}, enter column (0-{cols-1}) to play: "))
            if x < 0 or x >= cols:
                print("Invalid choice. Please try again.")
            # Here, we check each row to the bottom
            for row in range(rows-1, -1, -1):
                if arr[row][x] == '.':
                    arr[row][x] = player
                    return
            print("Column is full. Try a different one")
        except ValueError:
            print("Invalid input. Please enter an integer")
    
def checkWin(arr, rows, cols, player):
    # Check horizontal locations
    for c in range(cols-3):
        for r in range(rows):
            if arr[r][c] == player and arr[r][c+1] == player and arr[r][c+2] == player and arr[r][c+3] == player:
                return True

    # Check vertical locations
    for c in range(cols):
        for r in range(rows-3):
            if arr[r][c] == player and arr[r+1][c] == player and arr[r+2][c] == player and arr[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(cols-3):
        for r in range(rows-3):
            if arr[r][c] == player and arr[r+1][c+1] == player and arr[r+2][c+2] == player and arr[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(cols-3):
        for r in range(3, rows):
            if arr[r][c] == player and arr[r-1][c+1] == player and arr[r-2][c+2] == player and arr[r-3][c+3] == player:
                return True

    return False

def main():

    # Here's where we create out instances for a simple 2-player game
    rows, cols, board = create_board()
    print_board(board, cols)
    game_over = False
    turn = 0

    # This is where the game actually plays
    while game_over != True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_board(board, cols)
        if turn % 2 == 0:
            player_move(board, rows, cols, 1)
            if checkWin(board, rows, cols, '0'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print_board(board, cols)
                print("Player 1 wins!")
                game_over = True
        else:
            player_move(board, rows, cols, 2)
            if checkWin(board, rows, cols, 'X'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print_board(board, cols)
                print("Player 2 wins!")
                game_over = True

        if all(board[0][c] != '.' for c in range(cols)):
            os.system('cls' if os.name == 'nt' else 'clear')
            print_board(board, cols)
            print("It's a draw!")
            game_over = True
        
        turn += 1

if __name__ == '__main__':
    main()
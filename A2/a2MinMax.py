# In this file, we'll implement the MinMax algorithm. 
# Here, we can copy over the common functions that we've used.
from a2 import print_board, create_board, checkWin, os

def validMoves(arr, cols):
    return [col for col in range(cols) if arr[0][col] == '.']

def make_move(arr, rows, col, player):
    #print(f"Rows is {rows}")
    for row in range(rows-1, -1, -1):
        #print(f"Row is {row}")
        #print(f"Col is {col}")
        if arr[row][col] == '.':
            arr[row][col] = player
            break


def undo_move(arr, col):
    for row in range(len(arr)):
        if arr[row][col] != '.':
            arr[row][col] = '.'
            break

def player_move(arr, rows, cols, p_num):
    player = '0' if p_num == 1 else 'X'
    
    while True:
        try:
            x = int(input(f"Player {p_num}, enter column (0-{cols-1}) to play: "))
            if x < 0 or x >= cols:
                print("Invalid choice. Please try again.")
            for row in range(rows - 1, -1, -1):
                if arr[row][x] == '.':
                    arr[row][x] = player
                    return
            print("Column is full. Try a different one")
        except ValueError:
            print("Invalid input. Please enter an integer")

def evaluate_board(arr, rows, cols, player):
    score = 0
    opponent = 'X' if player == '0' else '0'
    for row in range(rows):
        for col in range(cols - 3):
            if arr[row][col:col + 4].count(player) == 3 and arr[row][col:col + 4].count('.') == 1:
                score += 5
            if arr[row][col:col + 4].count(opponent) == 3 and arr[row][col:col + 4].count('.') == 1:
                score -= 4

    for col in range(cols):
        for row in range(rows - 3):
            window = [arr[row + i][col] for i in range(4)]
            if window.count(player) == 3 and window.count('.') == 1:
                score += 5
            if window.count(opponent) == 3 and window.count('.') == 1:
                score -= 4

    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [arr[row + i][col + i] for i in range(4)]
            if window.count(player) == 3 and window.count('.') == 1:
                score += 5
            if window.count(opponent) == 3 and window.count('.') == 1:
                score -= 4

    for row in range(3, rows):
        for col in range(cols - 3):
            window = [arr[row - i][col + i] for i in range(4)]
            if window.count(player) == 3 and window.count('.') == 1:
                score += 5
            if window.count(opponent) == 3 and window.count('.') == 1:
                score -= 4

    return score

def computer_move(arr, rows, cols, player):
    # First, we need to make sure there are valid moves
    print("We're in here")
    valid_moves = validMoves(arr, cols)
    print(valid_moves)
    best_move = None
    best_score = float('-inf')


    for col in valid_moves:
        make_move(arr, rows, col, player)

        score = minmax(arr, 5, float('-inf'), float('inf'), False, rows, cols, player)

        undo_move(arr, col)

        if score > best_score:
            best_move = col
            best_score = score

    return best_move



def minmax(arr, depth, alpha, beta, maximizing_player, rows, cols, player):
    valid_moves = validMoves(arr, cols)
    if checkWin(arr, rows, cols, '0'):
        return 100 if player == '0' else -100
    elif checkWin(arr, rows, cols, 'X'):
        return 100 if player == 'X' else -100
    elif all(arr[0][c] != '.' for c in range(cols)):
        return 0
    
    if depth == 0:
        return evaluate_board(arr, rows, cols, player)
    
    if maximizing_player:
        max_eval = float('-inf')
        for col in valid_moves:
            make_move(arr, rows, col, player)
            eval = minmax(arr, depth -1, alpha, beta, False, rows, cols, player)
            undo_move(arr, col)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        opponent = 'X' if player == '0' else '0'
        for col in valid_moves:
            make_move(arr, rows, col, opponent)
            eval = minmax(arr, depth-1, alpha, beta, True, rows, cols, player)
            undo_move(arr, col)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval



def main():
    rows, cols, board = create_board()
    print_board(board, cols)
    game_over = False
    

    while True:
        first_player = input("Who goes first? Enter 'player' or 'bot': ")
        if first_player in ['player', 'bot']:
            break
        else:
            print("Please enter 'player' or 'bot' ")
    
    turn = 0 if first_player == 'player' else 1

    while not game_over:
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
            col = computer_move(board, rows, cols, 'X')
            make_move(board, rows, col, 'X') # Changed from cols to col here
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

main()
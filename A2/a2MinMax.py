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
    # This eval function essentially checks each "window" to see if there are 3 in a row. The more that there are, the the more the score goes up
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
    #print("We're in here")
    valid_moves = validMoves(arr, cols)
    #print(valid_moves)
    best_move = None
    best_score = float('-inf')

    # Next, we'll go through the valid moves and call the minmax function
    for col in valid_moves:
        make_move(arr, rows, col, player)

        score = minmax(arr, 5, float('-inf'), float('inf'), False, rows, cols, player)

        # Instead of creating a deep copy of every array, we'll just undo the move
        undo_move(arr, col)

        if score > best_score:
            best_move = col
            best_score = score

    return best_move



def minmax(arr, depth, alpha, beta, maximizing_player, rows, cols, player):
    # Make sure we don't run out of room
    valid_moves = validMoves(arr, cols)
    #As we recursively go through this function, if we hit a win/loss/draw condition, return the appropriate value
    if checkWin(arr, rows, cols, '0'):
        return 100 if player == '0' else -100
    elif checkWin(arr, rows, cols, 'X'):
        return 100 if player == 'X' else -100
    elif all(arr[0][c] != '.' for c in range(cols)):
        return 0
    
    if depth == 0:
        return evaluate_board(arr, rows, cols, player)
    

    # Here's where we incorporate move ordering. We're getting the scores from the evaluation function and putting them into a list
    move_scores = []
    for col in valid_moves:
        make_move(arr, rows, col, player)
        score = evaluate_board(arr, rows, cols, player)
        undo_move(arr, col)
        move_scores.append((col, score))

    # This is where we sort the list on whether if it's the maximizing player or not
    if maximizing_player:
        move_scores.sort(key=lambda x: x[1], reverse=True)
    else:
        move_scores.sort(key=lambda x: x[1])


    if maximizing_player:
        # Here we start the minmax "magic"
        # max_eval will be -inf
        max_eval = float('-inf')
        # Here we sort through the moves in the move_scores that we calculated earlier
        # We recursively go through the min max function getting all the possible scores until we reach our depth limit
        for col, _ in move_scores:
            make_move(arr, rows, col, player)
            eval = minmax(arr, depth -1, alpha, beta, False, rows, cols, player)
            undo_move(arr, col)
            max_eval = max(max_eval, eval)
            # Here's the alpha beta pruning
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        # Same thing as above, except it's for the not maximizing player
        min_eval = float('inf')
        opponent = 'X' if player == '0' else '0'
        for col, _ in move_scores:
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
    #print_board(board, cols)
    game_over = False
    
    # Player chooses who goes first
    while True:
        first_player = input("Who goes first? Enter 'player' or 'bot': ")
        if first_player in ['player', 'bot']:
            break
        else:
            print("Please enter 'player' or 'bot' ")
    
    turn = 0 if first_player == 'player' else 1

    # Where the game plays
    while not game_over:
        # Clear the screen so it's "cleaner" for the user
        os.system('cls' if os.name == 'nt' else 'clear')
        print_board(board, cols)
        if turn % 2 == 0:
            player_move(board, rows, cols, 1)
            if checkWin(board, rows, cols, '0'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print_board(board, cols)
                print("You win!")
                game_over = True
        else:
            col = computer_move(board, rows, cols, 'X')
            make_move(board, rows, col, 'X') # Changed from cols to col here
            if checkWin(board, rows, cols, 'X'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print_board(board, cols)
                print("The Bot wins!")
                game_over = True

        if all(board[0][c] != '.' for c in range(cols)):
            os.system('cls' if os.name == 'nt' else 'clear')
            print_board(board, cols)
            print("It's a draw!")
            game_over = True
        turn += 1

main()
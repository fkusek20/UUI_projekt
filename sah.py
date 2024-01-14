
import chess

def print_board_with_labels(board):
    board_string = str(board).split('\n')
    labeled_board = '\n'.join(f'{8-i} {row}' for i, row in enumerate(board_string))
    labeled_board += '\n  a b c d e f g h'
    return labeled_board

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -9999  # Black wins, negative value for white
        else:
            return 9999   # White wins, positive value for black
    if board.is_stalemate():
        return 0  # Draw

    # Simple material count for evaluation
    pawn = 1
    knight = 3
    bishop = 3
    rook = 5
    queen = 9
    score = 0
    for (piece, value) in [(chess.PAWN, pawn), (chess.KNIGHT, knight), (chess.BISHOP, bishop), (chess.ROOK, rook), (chess.QUEEN, queen)]:
        score += len(board.pieces(piece, chess.WHITE)) * value
        score -= len(board.pieces(piece, chess.BLACK)) * value
    return score
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, depth):
    best_move_found = None
    best_value = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move_found = move
            alpha = max(alpha, best_value)
    return best_move_found

# Glavni dio programa
board = chess.Board()
while not board.is_game_over():
    print(print_board_with_labels(board))  # Ispisuje ploču s oznakama
    if board.turn:  # Bijeli (AI)
        move = best_move(board, 3)  # Povećana dubina za bolji AI
        if move is None:
            print("Nema više legalnih poteza za AI.")
            break
        board.push(move)
    else:
        move = input("Vaš potez: ")
        try:
            board.push_san(move)
        except ValueError:
            print("Nevažeći potez, pokušajte ponovno.")
            continue
    print(print_board_with_labels(board))  # Ponovno ispisuje ploču nakon AI poteza

print("Kraj igre")
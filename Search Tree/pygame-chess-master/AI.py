
def get_opponent(player):
    if player == "white":
        return "black"
    else:
        return "white"

def evaluate_board(chess_board, player):
    values = {
        "white_king": 100000,
        "black_king": 100000,
        "white_queen": 9,
        "black_queen": 9,
        "white_rook": 5,
        "black_rook": 5,
        "white_bishop": 3,
        "black_bishop": 3,
        "white_knight": 3,
        "black_knight": 3,
        "white_pawn": 1,
        "black_pawn": 1
    }

    board = chess_board.piece_location
    player_score = 0
    opponent_score = 0

    pieces = []

    for col in board:
        for row in board[col]:
            piece = board[col][row][0]
            if piece != "":
                pieces.append(piece)

    for piece in pieces:
        if piece.startswith(player):
            player_score += values[piece]
        elif piece.startswith(get_opponent(player)):
            opponent_score += values[piece]

    return player_score - opponent_score


def all_possible_moves(chess_board, player):
    moves = []
    board = chess_board.piece_location # piece_location contains a value for every square on the board in format: [piece_name, currently_selected, x_y_coordinate]
    #print(board)
    for col in board:
        for row in board[col]:
            piece = board[col][row][0]
            if piece.startswith(player):
                piece_coord = board[col][row][2]
                possible_piece_moves = chess_board.possible_moves(piece, piece_coord)
                for move in possible_piece_moves:
                    source = col, row
                    moves.append((source, move))    # (Source co-ord of piece, destination co-ord of move)
    return moves


class ChessSearchTreeNode:
    def __init__(self, chess_board, playing_as, ply=0, max_depth=4):
        self.children = []
        self.value_assigned = False
        self.ply_depth = ply
        self.current_board = chess_board
        self.move_for = playing_as
        self.move = None  # stores the move made to this node. source, destination

        if self.current_board.winner != "":
            self.value = evaluate_board(self.current_board, self.move_for)
            self.value_assigned = True
        elif self.ply_depth >= max_depth:
            self.value = evaluate_board(self.current_board, self.move_for)
            self.value_assigned = True
        else:
            self.generate_children(max_depth)

    def generate_children(self, max_depth):
        for move in all_possible_moves(self.current_board, self.move_for):
            new_board = self.current_board.copy_board_state()
            source, destination = move
            new_board.apply_ai_move(source, destination)
            next_move = ChessSearchTreeNode(new_board, get_opponent(self.move_for), ply=self.ply_depth + 1, max_depth=max_depth)
            next_move.move = move  # store the move made to the node
            self.children.append(next_move)

    def min_max_value(self):
        if self.value_assigned:
            return self.value

        self.children.sort(key=lambda child: child.min_max_value())

        if (self.ply_depth % 2) == 0:
            # AI's move (max)
            self.value = self.children[-1].value
        else:
            # player's  move (min)
            self.value = self.children[0].value

        self.value_assigned = True
        return self.value

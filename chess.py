import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class ChessGame:
    def __init__(self):
        #Initialize the board wiwth standard chess setup using 2D array.
        #Uppercase letters represent white pieces, lowercase is black. Empty squares are '.'
        self.board = np.full((8,8),'.',dtype=str)

        self.board[1,:] = 'P' #white pawns
        self.board[6,:] = 'p' #black pawns

        #white pieces (bottom row)
        self.board[0,:] = ['R','N','B','Q','K','B','N','R']
        #black pieces (top row)
        self.board[7,:] = ['r','n','b','q','k','b','n','r']

        #game state variables
        self.current_player = 'white'
        self.game_over = False
        self.winner = None

        #track en passant
        self.en_passant_target = None

        #movement tracking
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rooks_moved = [False,False] #[queenside, kingside]
        self.black_rooks_moved = [False,False]

        #Position tracking for kings (for check detection)
        self.white_king_pos = (0,4)
        self.black_king_pos = (7,4)

        self.move_history = []

    def display_board(self):
        """Display chessboard using matplotlib"""
        #Terminal display
        print("\n    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        #print rows starting from top/black side
        for i in range(7, -1, -1):
            print(f"{i+1} |", end="")
            for j in range(8):
                piece = self.board[i][j]
                #display the piece (or space for empty square)
                piece_symbol = " " if piece == "." else piece
                print(f" {piece_symbol} |", end="")
            print("\n  +---+---+---+---+---+---+---+---+")

        print(f"\n{self.current_player.capitalize()}'s turn")

        #matplotlib display
        plt.figure(figsize=(8,8))

        #create chessboard pattern
        cmap = ListedColormap(['#f0d9b5','#b58863'])
        board_img = np.zeros((8,8))
        for i in range(8):
            for j in range(8):
                board_img[i,j]=(i+j)%2

        plt.imshow(board_img, cmap=cmap, origin='lower')

        # Define the Unicode chess symbols dictionary
        unicode_pieces = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }

        #place pieces on the board
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != '.':
                    plt.text(j,i,unicode_pieces[piece],
                             fontsize=28,ha='center',va='center',
                             color='black' if piece.isupper() else 'darkred')
        
        plt.xticks(np.arange(8), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        plt.yticks(np.arange(8), ['1', '2', '3', '4', '5', '6', '7', '8'])

        plt.title(f"{self.current_player.capitalize()}'s turn")

        plt.tight_layout()
        plt.pause(0.1)

    def algebraic_to_index(self, algebraic):
        """Convert algebraic notation to board indices"""
        if len(algebraic) != 2:
            return None
        col = ord(algebraic[0].lower()) - ord('a')
        row = int(algebraic[1]) - 1

        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None
    
    def index_to_algebraic(self, row, col):
        """Convert board indices to algebraic notation"""
        return chr(col +ord('a')) + str(row + 1)
    
    def is_valid_move(self, start, end):
        """Check if a move from start to end is valid"""
        start_row, start_col = start
        end_row, end_col = end

        #basic checks
        if start_row < 0 or start_row > 7 or start_col < 0 or start_col > 7:
            return False
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return False
        
        # get the piece at the start position
        piece = self.board[start_row][start_col]

        #check if there is a piece at the start position
        if piece == '.':
            return False
        
        #check if the piece belongs to the current player
        if (self.current_player == 'white' and not piece.isupper()) or (self.current_player == 'white' and piece.isupper()):
            return False
        
        end_piece = self.board[end_row][end_col]
        if end_piece != '.':
            if (piece.isupper() and end_piece.isupper()) or (piece.islower() and end_piece.islower()):
                return False
        
        #get the piece type
        piece_type = piece.lower()

        #check move validity based on piece type
        if piece_type == 'p': #Pawn
            return self.is_valid_pawn_move(start, end)
        elif piece_type == 'r': #rook
            return self.is_valid_rook_move(start, end)
        elif piece_type == 'n': #knight
            return self.is_valid_knight_move(start, end)
        elif piece_type == 'b': #bishop
            return self.is_valid_bishop_move(start, end)
        elif piece_type == 'q': #queen
            return self.is_valid_queen_move(start, end)
        elif piece_type == 'k': #king
            return self.is_valid_king_move(start, end)
        
        return False
    
    def is_valid_pawn_move(self, start, end):
        """Check if a pawn move is valid"""
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        end_piece = self.board[end_row][end_col]

        #direction depends on color
        direction = 1 if piece.isupper() else -1

        #normal move (one square forward)
        if start_col == end_col and end_piece == '.':
            if end_row == start_row + direction:
                return True
            
            #first move can be two squares
            if (piece.isupper() and start_row == 1 and end_row == 3) or (piece.isupper() and start_row == 6 and end_row == 4):
                #check if the path is clear
                if self.board[start_row + direction][start_col] == '.':
                    return True
                
        #capture move (diagnol)
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if end_piece != '.' and ((piece.isupper() and end_piece.islower()) or (piece.islower() and end_piece.isupper())):
                return True
            elif end_piece == '.' and (end_row, end_col) == self.en_passant_target:
                return True

        return False
    
    def is_valid_rook_move(self, start, end):
        """Check if a rook move is valid"""
        start_row, start_col = start
        end_row, end_col = end

        #Rooks can only move in straight lines
        if start_row != end_row and start_col != end_col:
            return False
        
        return self.is_path_clear(start, end)
    
    def is_valid_knight_move(self, start, end):
        """Check if a knight move is valid"""
        start_row, start_col = start
        end_row, end_col = end

        #Knights look like horses, yes, it's true! 
        #Pay close attention, or they'll jump over you!
        #Hop hop, and to the side, is how they go!
        #In the shape of an L is how they flow!

        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        #No check for clear path because knights can jump over other pieces
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def is_valid_bishop_move(self, start, end):
        """Check if a bishop move is valid"""
        start_row, start_col = start
        end_row, end_col = end

        #Diagonal movement
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        
        return self.is_path_clear(start, end)
    
    def is_valid_queen_move(self, start, end):
        """Check if a queen move is valid"""
        #Combine rook and bishop checks
        return self.is_valid_bishop_move(start, end) or self.is_valid_rook_move(start, end)
    
    def is_valid_king_move(self, start, end):
        """Check if a king move is valid"""
        start_row, start_col = start
        end_row, end_col = end

        #Kings move one square in any direction
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        #normal king move
        if row_diff <= 1 and col_diff <= 1:
            return True

        #TODO: Castling

        return False

    def is_path_clear(self, start, end):
        """Check if the path between start and end is clear of pieces"""
        start_row, start_col = start
        end_row, end_col = end

        #Determine the direction of movement
        row_step = 0 if start_row == end_row else (1 if start_row < end_row else -1)
        col_step = 0 if start_col == end_col else (1 if start_col < end_col else -1)

        #Check each square along the path (excluding start and end)
        row, col = start_row + row_step, start_col + col_step
        while (row, col) != (end_row, end_col):
            if self.board[row][col] != '.':
                return False
            row += row_step
            col += col_step

        return True
    
    def make_move(self, start_pos, end_pos):
        """Make a move from start_pos to end_pos if valid"""
        #Convert algebraic notation to board indices
        if isinstance(start_pos, str):
            start = self.algebraic_to_index(start_pos)
            if start is None:
                return False, "Invalid start position notation"
        else:
            start = start_pos

        if isinstance(end_pos, str):
            end = self.algebraic_to_index(end_pos)
            if end is None:
                return False, "Invalid end position notation"
            
        else:
            end = end_pos

        #Save the current state for undoing
        moved_piece = self.board[start[0]][start[1]]
        captured_piece = self.board[end[0]][end[1]]
        self.move_history.append((start, end, moved_piece, captured_piece))

        start_row, start_col = start
        end_row, end_col = end

        #En passant
        if moved_piece.lower() == 'p':
            direction = 1 if moved_piece.isupper() else -1
            if abs(end_row - start_row) == 2:
                self.en_passant_target = (start_row + direction, start_col)
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None

        #Update king position if king is moved
        if moved_piece.lower() == 'k':
            if moved_piece.isupper(): #white king
                self.white_king_pos = end
                self.white_rooks_moved = True
            else: #black king
                self.black_king_pos = end
                self.black_king_moved = True

        #Update rook moved status for castling
        if moved_piece.lower() == 'r':
            if start[0] == 0: #white rooks
                if start[1] == 0: #queenside
                    self.white_rooks_moved[0] = True
                elif start[1] == 7: #kingside
                    self.white_rooks_moved[1] = True
            elif start[0] == 7: #black rooks
                if start[1] == 0: #queenside
                    self.black_rooks_moved[0] = True
                elif start[1] == 7: #kingside
                    self.black_rooks_moved[1] = True

        #make the move
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = '.'

        #TODO: Handle special moves like castling, en passant, and promotion

        #Check for game ending conditions
        #TODO: implement check, checkmate, and stalemate detection

        #Switch the current player
        self.current_player = 'black' if self.current_player == 'white' else 'white'

        return True, "Move successful"
    
    def undo_move(self):
        """Undo the last move"""
        if not self.move_history:
            return False, "No moves to undo"
        
        #Get the last move
        start, end, moved_piece, captured_piece = self.move_history.pop()

        #Restore the board state
        self.board[start[0]][start[1]] = moved_piece
        self.board[end[0]][end[1]] = captured_piece

        #Update king position if king was moved
        if moved_piece.lower() == 'k':
            if moved_piece.isupper(): #white king
                self.white_king_pos = start
                #Reset king moved status if this was the first king move
                if not self.move_history or all(m[2].lower() != 'k' or not m[2].isupper() for m in self.move_history):
                    self.white_king_moved = False
            else: #black king
                self.black_king_pos = start
                #reset king moved status if this was the first king move
                if not self.move_history or all(m[2].lower() != 'k' or m[2].isupper() for m in self.move_history):
                    self.black_king_moved = False

        #switch the current player back
        self.current_player = 'black' if self.current_player == 'white' else 'white'

        return True, "Move undone"
    
def play_chess():
    """Main game function to play chess"""
    game = ChessGame()

    print("Welcome to Python Chess!")
    print("Enter moves in algebraic notation, e.g., 'e2 e4'")
    print("Type 'quit' to exit, 'undo' to undo the last move")

    try:
        plt.ion() #Turn on interactive mode with matplotlib
    except:
        pass

    #display initial board
    game.display_board()

    while not game.game_over:
        #get player input
        move_input = input(f"{game.current_player.capitalize()}'s move:")

        #process commands
        if move_input.lower() == 'quit':
            break
        elif move_input.lower == 'undo':
            success, message = game.undo_move()
            print(message)
            #display updated board after undoing
            game.display_board()
            continue

        #parse the move input
        try:
            start_pos, end_pos = move_input.split()
            success, message = game.make_move(start_pos, end_pos)
            if not success:
                print(message)
            else:
                #clear screen in terminal
                print("\033[H\033[J]]", end="")
                #display the updated board after a successful move
                game.display_board()
        except ValueError:
            print("Invalid input format. Use 'start_pos end_pos', e.g., 'e2 e4'")

    #Game over
    if game.game_over:
        print(f"Game over! {game.winner} wins!")
    else:
        print("Thanks for playing!")

    try:
        plt.ioff() #Turn off interactive mode
    except:
        pass

#Run the game when the script is executed
if __name__ == "__main__":
    play_chess()
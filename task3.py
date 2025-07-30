import streamlit as st
import numpy as np
from typing import List, Tuple, Optional

class ChessGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'white'
        self.selected_square = None
        self.game_over = False
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.en_passant_target = None
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.in_check = False
        self.checkmate = False
        self.stalemate = False

    def initialize_board(self):
        """Initialize the chess board with pieces in starting positions"""
        board = [['' for _ in range(8)] for _ in range(8)]
        
        # Set up pawns
        for col in range(8):
            board[1][col] = '♟'  # Black pawns
            board[6][col] = '♙'  # White pawns
        
        # Set up other pieces
        black_pieces = ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']
        white_pieces = ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        
        for col in range(8):
            board[0][col] = black_pieces[col]
            board[7][col] = white_pieces[col]
        
        return board

    def get_piece_color(self, piece: str) -> Optional[str]:
        """Determine if a piece is white or black"""
        if piece in ['♙', '♖', '♘', '♗', '♕', '♔']:
            return 'white'
        elif piece in ['♟', '♜', '♞', '♝', '♛', '♚']:
            return 'black'
        return None

    def get_king_position(self, color: str) -> Tuple[int, int]:
        """Find the position of the king for a given color"""
        king_piece = '♔' if color == 'white' else '♚'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    return (row, col)
        return None

    def is_square_under_attack(self, row: int, col: int, attacking_color: str) -> bool:
        """Check if a square is under attack by the given color"""
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and self.get_piece_color(piece) == attacking_color:
                    if self.is_valid_move_internal(r, c, row, col, attacking_color):
                        return True
        return False

    def is_king_in_check(self, color: str) -> bool:
        """Check if the king is in check"""
        king_pos = self.get_king_position(color)
        if king_pos:
            return self.is_square_under_attack(king_pos[0], king_pos[1], 
                                             'black' if color == 'white' else 'white')
        return False

    def is_valid_move_internal(self, start_row: int, start_col: int, end_row: int, end_col: int, player: str) -> bool:
        """Internal move validation without considering check"""
        if start_row == end_row and start_col == end_col:
            return False
        
        start_piece = self.board[start_row][start_col]
        end_piece = self.board[end_row][end_col]
        
        # Check if start square has a piece
        if not start_piece:
            return False
        
        # Check if piece belongs to current player
        if self.get_piece_color(start_piece) != player:
            return False
        
        # Check if end square has own piece
        if end_piece and self.get_piece_color(end_piece) == player:
            return False
        
        piece_type = start_piece
        
        # Pawn moves
        if piece_type in ['♙', '♟']:
            direction = -1 if player == 'white' else 1
            if start_col == end_col:  # Forward move
                if end_row == start_row + direction and not end_piece:
                    return True
                if (player == 'white' and start_row == 6 and end_row == 4 and not end_piece and not self.board[5][start_col]):
                    return True
                if (player == 'black' and start_row == 1 and end_row == 3 and not end_piece and not self.board[2][start_col]):
                    return True
            elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
                if end_piece:  # Capture
                    return True
                # En passant
                if self.en_passant_target and (end_row, end_col) == self.en_passant_target:
                    return True
            return False
        
        # Rook moves
        elif piece_type in ['♖', '♜']:
            if start_row == end_row or start_col == end_col:
                if start_row == end_row:
                    start, end = min(start_col, end_col), max(start_col, end_col)
                    for col in range(start + 1, end):
                        if self.board[start_row][col]:
                            return False
                else:
                    start, end = min(start_row, end_row), max(start_row, end_row)
                    for row in range(start + 1, end):
                        if self.board[row][start_col]:
                            return False
                return True
        
        # Bishop moves
        elif piece_type in ['♗', '♝']:
            if abs(start_row - end_row) == abs(start_col - end_col):
                row_dir = 1 if end_row > start_row else -1
                col_dir = 1 if end_col > start_col else -1
                row, col = start_row + row_dir, start_col + col_dir
                while row != end_row and col != end_col:
                    if self.board[row][col]:
                        return False
                    row += row_dir
                    col += col_dir
                return True
        
        # Queen moves
        elif piece_type in ['♕', '♛']:
            # Rook-like move
            if start_row == end_row or start_col == end_col:
                if start_row == end_row:
                    start, end = min(start_col, end_col), max(start_col, end_col)
                    for col in range(start + 1, end):
                        if self.board[start_row][col]:
                            return False
                else:
                    start, end = min(start_row, end_row), max(start_row, end_row)
                    for row in range(start + 1, end):
                        if self.board[row][start_col]:
                            return False
                return True
            # Bishop-like move
            elif abs(start_row - end_row) == abs(start_col - end_col):
                row_dir = 1 if end_row > start_row else -1
                col_dir = 1 if end_col > start_col else -1
                row, col = start_row + row_dir, start_col + col_dir
                while row != end_row and col != end_col:
                    if self.board[row][col]:
                        return False
                    row += row_dir
                    col += col_dir
                return True
        
        # King moves
        elif piece_type in ['♔', '♚']:
            # Castling
            if start_col == 4 and abs(end_col - start_col) == 2 and start_row == end_row:
                if end_col == 6:  # Kingside castling
                    if self.castling_rights[player]['kingside']:
                        if not any(self.board[start_row][c] for c in [5, 6]):
                            if not self.is_square_under_attack(start_row, 4, 'black' if player == 'white' else 'white'):
                                if not self.is_square_under_attack(start_row, 5, 'black' if player == 'white' else 'white'):
                                    if not self.is_square_under_attack(start_row, 6, 'black' if player == 'white' else 'white'):
                                        return True
                elif end_col == 2:  # Queenside castling
                    if self.castling_rights[player]['queenside']:
                        if not any(self.board[start_row][c] for c in [1, 2, 3]):
                            if not self.is_square_under_attack(start_row, 4, 'black' if player == 'white' else 'white'):
                                if not self.is_square_under_attack(start_row, 3, 'black' if player == 'white' else 'white'):
                                    if not self.is_square_under_attack(start_row, 2, 'black' if player == 'white' else 'white'):
                                        return True
            # Normal king move
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
        
        # Knight moves
        elif piece_type in ['♘', '♞']:
            row_diff = abs(start_row - end_row)
            col_diff = abs(start_col - end_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        
        return False

    def is_valid_move(self, start_row: int, start_col: int, end_row: int, end_col: int, player: str) -> bool:
        """Check if a move is valid including check considerations"""
        if not self.is_valid_move_internal(start_row, start_col, end_row, end_col, player):
            return False
        
        # Make temporary move to check if it leaves king in check
        temp_board = [row[:] for row in self.board]
        temp_board[end_row][end_col] = temp_board[start_row][start_col]
        temp_board[start_row][start_col] = ''
        
        # Find king position after move
        king_piece = '♔' if player == 'white' else '♚'
        king_pos = None
        for r in range(8):
            for c in range(8):
                if temp_board[r][c] == king_piece:
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        
        if king_pos:
            # Check if king would be in check after move
            opponent = 'black' if player == 'white' else 'white'
            return not self.is_square_under_attack(king_pos[0], king_pos[1], opponent)
        
        return True

    def make_move(self, start_row: int, start_col: int, end_row: int, end_col: int):
        """Make a move on the board"""
        start_piece = self.board[start_row][start_col]
        end_piece = self.board[end_row][end_col]
        
        # Capture piece
        if end_piece:
            captured_color = self.get_piece_color(end_piece)
            self.captured_pieces[captured_color].append(end_piece)
        
        # Handle castling
        if start_piece in ['♔', '♚'] and abs(end_col - start_col) == 2:
            if end_col == 6:  # Kingside castling
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = ''
            elif end_col == 2:  # Queenside castling
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = ''
        
        # Handle en passant capture
        if start_piece in ['♙', '♟'] and self.en_passant_target and (end_row, end_col) == self.en_passant_target:
            captured_row = start_row
            captured_color = 'black' if self.current_player == 'white' else 'white'
            captured_piece = '♟' if captured_color == 'black' else '♙'
            self.captured_pieces[captured_color].append(captured_piece)
            self.board[captured_row][end_col] = ''
        
        # Move piece
        self.board[end_row][end_col] = start_piece
        self.board[start_row][start_col] = ''
        
        # Handle pawn promotion
        if start_piece in ['♙', '♟'] and end_row in [0, 7]:
            self.board[end_row][end_col] = '♕' if self.current_player == 'white' else '♛'
        
        # Update en passant target
        if start_piece in ['♙', '♟'] and abs(end_row - start_row) == 2:
            self.en_passant_target = ((start_row + end_row) // 2, start_col)
        else:
            self.en_passant_target = None
        
        # Update castling rights
        if start_piece in ['♔', '♚']:
            self.castling_rights[self.current_player]['kingside'] = False
            self.castling_rights[self.current_player]['queenside'] = False
        elif start_piece in ['♖', '♜']:
            if start_col == 0:  # Queenside rook
                self.castling_rights[self.current_player]['queenside'] = False
            elif start_col == 7:  # Kingside rook
                self.castling_rights[self.current_player]['kingside'] = False

    def get_legal_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all legal moves for a piece at the given position"""
        legal_moves = []
        piece = self.board[row][col]
        if piece and self.get_piece_color(piece) == self.current_player:
            for r in range(8):
                for c in range(8):
                    if self.is_valid_move(row, col, r, c, self.current_player):
                        legal_moves.append((r, c))
        return legal_moves

    def is_checkmate(self) -> bool:
        """Check if the current player is in checkmate"""
        if not self.is_king_in_check(self.current_player):
            return False
        
        # Check if any move can get out of check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.get_piece_color(piece) == self.current_player:
                    for r in range(8):
                        for c in range(8):
                            if self.is_valid_move(row, col, r, c, self.current_player):
                                return False
        return True

    def is_stalemate(self) -> bool:
        """Check if the current player is in stalemate"""
        if self.is_king_in_check(self.current_player):
            return False
        
        # Check if any legal move exists
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.get_piece_color(piece) == self.current_player:
                    for r in range(8):
                        for c in range(8):
                            if self.is_valid_move(row, col, r, c, self.current_player):
                                return False
        return True

    def handle_square_click(self, row: int, col: int):
        """Handle click on a chess square"""
        if self.game_over:
            return
        
        piece = self.board[row][col]
        
        # If no square is selected, select this square if it has a piece of current player
        if self.selected_square is None:
            if piece and self.get_piece_color(piece) == self.current_player:
                self.selected_square = (row, col)
        else:
            # If a square is already selected, try to make a move
            start_row, start_col = self.selected_square
            
            if self.is_valid_move(start_row, start_col, row, col, self.current_player):
                # Make the move
                self.make_move(start_row, start_col, row, col)
                
                # Add to move history
                move_notation = f"{chr(97+start_col)}{8-start_row}-{chr(97+col)}{8-row}"
                self.move_history.append(f"{self.current_player}: {move_notation}")
                
                # Check for check/checkmate/stalemate
                next_player = 'black' if self.current_player == 'white' else 'white'
                self.in_check = self.is_king_in_check(next_player)
                self.checkmate = self.is_checkmate()
                self.stalemate = self.is_stalemate()
                
                if self.checkmate:
                    self.game_over = True
                elif self.stalemate:
                    self.game_over = True
                
                # Switch players
                self.current_player = next_player
            
            self.selected_square = None

    def reset_game(self):
        """Reset the game to initial state"""
        self.board = self.initialize_board()
        self.current_player = 'white'
        self.selected_square = None
        self.game_over = False
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.en_passant_target = None
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.in_check = False
        self.checkmate = False
        self.stalemate = False

# Initialize session state
if 'chess_game' not in st.session_state:
    st.session_state.chess_game = ChessGame()

game = st.session_state.chess_game

# Streamlit UI
st.title("♔ Advanced Chess Game - Best Code")
st.markdown("---")

# Game status
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    status_color = "red" if game.in_check else "green"
    status_text = "♔ White" if game.current_player == 'white' else "♚ Black"
    if game.checkmate:
        status_text += " - CHECKMATE!"
    elif game.stalemate:
        status_text += " - STALEMATE!"
    elif game.in_check:
        status_text += " - IN CHECK!"
    
    st.markdown(f"<h3 style='color: {status_color}; text-align: center;'>{status_text}</h3>", unsafe_allow_html=True)
    
    if st.button("🔄 Reset Game", use_container_width=True):
        game.reset_game()

# Main game area
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("### Chess Board")
    
    # Create the chess board with enhanced styling
    for row in range(8):
        cols = st.columns(8)
        for col in range(8):
            with cols[col]:
                # Determine square color
                is_light_square = (row + col) % 2 == 0
                square_color = "#F0D9B5" if is_light_square else "#B58863"
                
                # Highlight selected square
                if game.selected_square == (row, col):
                    square_color = "#FFD700"  # Gold for selected
                
                # Highlight legal moves
                legal_moves = game.get_legal_moves(game.selected_square[0], game.selected_square[1]) if game.selected_square else []
                if (row, col) in legal_moves:
                    square_color = "#90EE90"  # Light green for legal moves
                
                # Get piece
                piece = game.board[row][col]
                display_text = piece if piece else " "
                
                # Create button for each square with enhanced styling
                button_style = f"""
                <style>
                .chess-button {{
                    background-color: {square_color};
                    border: 2px solid #333;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 20px;
                    font-weight: bold;
                    width: 100%;
                    height: 50px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                
                if st.button(display_text, key=f"square_{row}_{col}", 
                            help=f"Row {row+1}, Column {chr(97+col)}"):
                    game.handle_square_click(row, col)

# Side panels
with col1:
    st.markdown("### Captured Pieces")
    st.markdown("**White captured:**")
    for piece in game.captured_pieces['white']:
        st.write(f" {piece}")
    
    st.markdown("**Black captured:**")
    for piece in game.captured_pieces['black']:
        st.write(f" {piece}")

with col3:
    st.markdown("### Move History")
    if game.move_history:
        for i, move in enumerate(game.move_history[-15:], 1):  # Show last 15 moves
            st.write(f"{i}. {move}")
    else:
        st.write("No moves yet")

# Instructions and features
st.markdown("---")
st.markdown("""
### 🎯 Advanced Features:
- **Check Detection**: Automatically detects when king is in check
- **Checkmate Detection**: Game ends when king is checkmated
- **Stalemate Detection**: Game ends in draw when no legal moves
- **Castling**: Kingside and queenside castling with proper validation
- **En Passant**: Pawn capture en passant
- **Pawn Promotion**: Pawns automatically promote to queens
- **Move Highlighting**: Legal moves are highlighted in green
- **Captured Pieces**: Track all captured pieces
- **Move History**: Complete move history with notation

### 🎮 How to Play:
1. Click on a piece to select it (highlighted in gold)
2. Legal moves are highlighted in green
3. Click on a destination square to move
4. Players alternate turns (White goes first)
5. Game ends on checkmate or stalemate

### ♟️ Piece Legend:
- ♔♚: Kings
- ♕♛: Queens  
- ♖♜: Rooks
- ♗♝: Bishops
- ♘♞: Knights
- ♙♟: Pawns
""")

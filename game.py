# game.py
import streamlit as st
import numpy as np

class GamePiece:
    def __init__(self, team, piece_type):
        self.team = team  # 'H' for Horatii, 'C' for Curiatii
        self.piece_type = piece_type
        self.emoji = self.get_emoji()
    
    def get_emoji(self):
        emoji_map = {
            ('H', 'S'): '⚔️',  # Horatii Swordsman
            ('H', 'L'): '🗡️',  # Horatii Spearman
            ('H', 'A'): '🏹',  # Horatii Archer
            ('C', 'S'): '⚔️',  # Curiatii Swordsman
            ('C', 'L'): '🗡️',  # Curiatii Spearman
            ('C', 'A'): '🏹',  # Curiatii Archer
        }
        return emoji_map.get((self.team, self.piece_type))

class GameBoard:
    def __init__(self):
        self.board_size = 8
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.setup_armies()
        self.selected_piece = None
    
    def setup_armies(self):
        # Setup formations
        formations = {
            'H': (0, [  # Horatii at top
                ['A', 'A', 'A'],
                ['L', 'L', 'L'],
                ['S', 'S', 'S']
            ]),
            'C': (5, [  # Curiatii at bottom
                ['A', 'A', 'A'],
                ['L', 'L', 'L'],
                ['S', 'S', 'S']
            ])
        }
        
        for team, (start_row, formation) in formations.items():
            start_col = (self.board_size - 3) // 2
            for i, row in enumerate(formation):
                for j, piece_type in enumerate(row):
                    self.board[start_row + i][start_col + j] = GamePiece(team, piece_type)

# app.py
import streamlit as st
from game import GameBoard

def main():
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    # Initialize game board in session state
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None
    
    # Create a grid display
    col1, col2 = st.columns([3, 1])
    
    with col1:
        for i in range(8):
            cols = st.columns(8)
            for j in range(8):
                with cols[j]:
                    cell_color = '#FFFFFF' if (i + j) % 2 == 0 else '#A9A9A9'
                    piece = st.session_state.game_board.board[i][j]
                    
                    # Create clickable button for each cell
                    if piece:
                        text_color = '#0000FF' if piece.team == 'H' else '#FF0000'
                        if st.button(
                            piece.emoji,
                            key=f"cell_{i}_{j}",
                            help=f"{'Horácio' if piece.team == 'H' else 'Curiácio'}"
                        ):
                            if st.session_state.selected_pos is None:
                                # Select piece
                                st.session_state.selected_pos = (i, j)
                            else:
                                # Move piece
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
                    else:
                        if st.button(
                            "　",  # Empty space
                            key=f"cell_{i}_{j}"
                        ):
                            if st.session_state.selected_pos is not None:
                                # Move piece to empty cell
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
    
    with col2:
        st.write("Legenda:")
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        st.write("\nAzul - Horácios")
        st.write("Vermelho - Curiácios")
        
        if st.session_state.selected_pos is not None:
            i, j = st.session_state.selected_pos
            piece = st.session_state.game_board.board[i][j]
            st.write("\nPeça selecionada:")
            st.write(f"{'Horácio' if piece.team == 'H' else 'Curiácio'} {piece.emoji}")
            if st.button("Cancelar seleção"):
                st.session_state.selected_pos = None
                st.rerun()

if __name__ == "__main__":
    main()

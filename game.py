# game.py
import streamlit as st
import numpy as np

class GameBoard:
    def __init__(self):
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size), dtype=object)
        self.setup_armies()
    
    def setup_armies(self):
        # Define piece types
        pieces = {
            'S': 'Espadachim',  # Swordsman
            'L': 'Lanceiro',    # Spearman
            'A': 'Arqueiro'     # Archer
        }
        
        # Setup Horatii (top army)
        self.place_army(2, pieces, 'H')  # H for Horatii
        
        # Setup Curiatii (bottom army)
        self.place_army(5, pieces, 'C')  # C for Curiatii
    
    def place_army(self, row, pieces, army_prefix):
        # Formation setup (3x3)
        formation = [
            ['A', 'A', 'A'],    # Archers in back
            ['L', 'L', 'L'],    # Spearmen in middle
            ['S', 'S', 'S']     # Swordsmen in front
        ]
        
        # Calculate starting column to center the formation
        start_col = (self.board_size - 3) // 2
        
        for i, row_formation in enumerate(formation):
            for j, piece in enumerate(row_formation):
                self.board[row + i - 1][start_col + j] = f"{army_prefix}-{piece}"

# app.py
import streamlit as st
from game import GameBoard

def main():
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    # Initialize game board
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
    
    # Display the game board
    board = st.session_state.game_board.board
    
    # Create a grid display
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display the chess-like board
        for i in range(8):
            cols = st.columns(8)
            for j in range(8):
                with cols[j]:
                    cell_color = 'white' if (i + j) % 2 == 0 else 'gray'
                    piece = board[i][j]
                    if piece:
                        # Display piece with background color
                        st.markdown(
                            f"""
                            <div style="
                                background-color: {cell_color};
                                padding: 20px;
                                text-align: center;
                                color: {'blue' if 'H' in str(piece) else 'red'};
                                font-weight: bold;
                            ">
                                {piece}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        # Empty cell with background color
                        st.markdown(
                            f"""
                            <div style="
                                background-color: {cell_color};
                                padding: 20px;
                                text-align: center;
                            ">
                                &nbsp;
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    
    with col2:
        st.write("Legenda:")
        st.write("H-S: Horácio Espadachim")
        st.write("H-L: Horácio Lanceiro")
        st.write("H-A: Horácio Arqueiro")
        st.write("C-S: Curiácio Espadachim")
        st.write("C-L: Curiácio Lanceiro")
        st.write("C-A: Curiácio Arqueiro")

if __name__ == "__main__":
    main()

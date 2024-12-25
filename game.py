# game.py
import streamlit as st
import numpy as np

class GameBoard:
    def __init__(self):
        self.board_size = 8
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.setup_armies()
        self.selected_piece = None

    def setup_armies(self):
        # Define as peças com seus emojis
        pieces = {
            'H': {  # Horácios (azul)
                'S': '⚔️',  # Espadachim
                'L': '🗡️',  # Lanceiro
                'A': '🏹'   # Arqueiro
            },
            'C': {  # Curiácios (vermelho)
                'S': '⚔️',  # Espadachim
                'L': '🗡️',  # Lanceiro
                'A': '🏹'   # Arqueiro
            }
        }

        # Formação inicial (3x3)
        formation = [
            ['A', 'A', 'A'],  # Arqueiros atrás
            ['L', 'L', 'L'],  # Lanceiros no meio
            ['S', 'S', 'S']   # Espadachins na frente
        ]

        # Posiciona Horácios (topo)
        start_row = 0
        start_col = (self.board_size - 3) // 2
        for i, row in enumerate(formation):
            for j, piece_type in enumerate(row):
                self.board[start_row + i][start_col + j] = {
                    'team': 'H',
                    'type': piece_type,
                    'emoji': pieces['H'][piece_type]
                }

        # Posiciona Curiácios (base)
        start_row = 5
        for i, row in enumerate(formation):
            for j, piece_type in enumerate(row):
                self.board[start_row + i][start_col + j] = {
                    'team': 'C',
                    'type': piece_type,
                    'emoji': pieces['C'][piece_type]
                }

def main():
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    # Inicializa o tabuleiro na sessão
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None
    
    # Cria o display do tabuleiro
    col1, col2 = st.columns([3, 1])
    
    with col1:
        for i in range(8):
            cols = st.columns(8)
            for j in range(8):
                with cols[j]:
                    cell_color = '#FFFFFF' if (i + j) % 2 == 0 else '#A9A9A9'
                    piece = st.session_state.game_board.board[i][j]
                    
                    if piece:
                        text_color = '#0000FF' if piece['team'] == 'H' else '#FF0000'
                        if st.button(
                            piece['emoji'],
                            key=f"cell_{i}_{j}",
                            help=f"{'Horácio' if piece['team'] == 'H' else 'Curiácio'}"
                        ):
                            if st.session_state.selected_pos is None:
                                st.session_state.selected_pos = (i, j)
                            else:
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
                    else:
                        if st.button(
                            "　",  # Espaço vazio
                            key=f"cell_{i}_{j}"
                        ):
                            if st.session_state.selected_pos is not None:
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
            st.write(f"{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}")
            if st.button("Cancelar seleção"):
                st.session_state.selected_pos = None
                st.rerun()

if __name__ == "__main__":
    main()

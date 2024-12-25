import streamlit as st
import numpy as np

class GameBoard:
    def __init__(self):
        self.board_size_x = 7  # Largura do tabuleiro
        self.board_size_y = 8  # Altura do tabuleiro
        self.board = [[None for _ in range(self.board_size_x)] for _ in range(self.board_size_y)]
        self.setup_armies()
        self.selected_piece = None

    def setup_armies(self):
        # Define as peças com seus emojis e cores
        pieces = {
            'H': {  # Horácios (azul)
                'S': {'emoji': '⚔️', 'color': '#0000FF'},
                'L': {'emoji': '🗡️', 'color': '#0000FF'},
                'A': {'emoji': '🏹', 'color': '#0000FF'}
            },
            'C': {  # Curiácios (vermelho)
                'S': {'emoji': '⚔️', 'color': '#FF0000'},
                'L': {'emoji': '🗡️', 'color': '#FF0000'},
                'A': {'emoji': '🏹', 'color': '#FF0000'}
            }
        }

        # Formação inicial Horácios (3x3) - topo
        formation_horatii = [
            ['A', 'A', 'A'],  # Arqueiros atrás
            ['L', 'L', 'L'],  # Lanceiros no meio
            ['S', 'S', 'S']   # Espadachins na frente
        ]

        # Formação inicial Curiácios (3x3) - base (invertida)
        formation_curiatii = [
            ['S', 'S', 'S'],  # Espadachins atrás
            ['L', 'L', 'L'],  # Lanceiros no meio
            ['A', 'A', 'A']   # Arqueiros na frente
        ]

        # Posiciona Horácios (topo)
        start_row = 0
        start_col = (self.board_size_x - 3) // 2
        for i, row in enumerate(formation_horatii):
            for j, piece_type in enumerate(row):
                self.board[start_row + i][start_col + j] = {
                    'team': 'H',
                    'type': piece_type,
                    'emoji': pieces['H'][piece_type]['emoji'],
                    'color': pieces['H'][piece_type]['color']
                }

        # Posiciona Curiácios (base)
        start_row = 5
        for i, row in enumerate(formation_curiatii):
            for j, piece_type in enumerate(row):
                self.board[start_row + i][start_col + j] = {
                    'team': 'C',
                    'type': piece_type,
                    'emoji': pieces['C'][piece_type]['emoji'],
                    'color': pieces['C'][piece_type]['color']
                }

def main():
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    # Inicializa o tabuleiro na sessão
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None
    
    # Layout com duas colunas
    col1, col2 = st.columns([3, 1])
    
    # Tabuleiro (coluna 1)
    with col1:
        for i in range(8):
            cols = st.columns(7)  # Reduzido para 7 colunas
            for j in range(7):    # Reduzido para 7 colunas
                with cols[j]:
                    cell_color = '#DEB887' if (i + j) % 2 == 0 else '#8B4513'
                    piece = st.session_state.game_board.board[i][j]
                    
                    if piece:
                        if st.button(
                            piece['emoji'],
                            key=f"cell_{i}_{j}",
                            help=f"{'Horácio' if piece['team'] == 'H' else 'Curiácio'}",
                            use_container_width=True
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
                            " ",
                            key=f"cell_{i}_{j}",
                            use_container_width=True
                        ):
                            if st.session_state.selected_pos is not None:
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
    
    # Legenda e controles (coluna 2)
    with col2:
        st.write("Legenda:")
        
        # Horácios (azul)
        st.markdown("<div style='color: #0000FF;'>Horácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("") # Espaço em branco
        
        # Curiácios (vermelho)
        st.markdown("<div style='color: #FF0000;'>Curiácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("") # Espaço em branco
        
        # Informações sobre peça selecionada
        if st.session_state.selected_pos is not None:
            i, j = st.session_state.selected_pos
            piece = st.session_state.game_board.board[i][j]
            st.write("\nPeça selecionada:")
            st.markdown(f"<p style='color: {piece['color']};'>{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}</p>", unsafe_allow_html=True)
            if st.button("❌ Cancelar seleção"):
                st.session_state.selected_pos = None
                st.rerun()
        
        st.write("") # Espaço em branco
        
        # Botão de reinício abaixo da legenda
        if st.button("🔄 Reiniciar Jogo"):
            st.session_state.game_board = GameBoard()
            st.session_state.selected_pos = None
            st.rerun()

if __name__ == "__main__":
    main()

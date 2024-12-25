import streamlit as st
import numpy as np

class GameBoard:
    def __init__(self):
        self.board_size = 8
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.setup_armies()
        self.selected_piece = None

    def setup_armies(self):
        # Define as peças com seus emojis e cores
        pieces = {
            'H': {  # Horácios (azul)
                'S': {'emoji': '⚔️', 'color': '#0000FF'},  # Azul forte
                'L': {'emoji': '🗡️', 'color': '#0000FF'},
                'A': {'emoji': '🏹', 'color': '#0000FF'}
            },
            'C': {  # Curiácios (vermelho)
                'S': {'emoji': '⚔️', 'color': '#FF0000'},  # Vermelho forte
                'L': {'emoji': '🗡️', 'color': '#FF0000'},
                'A': {'emoji': '🏹', 'color': '#FF0000'}
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
                    'emoji': pieces['H'][piece_type]['emoji'],
                    'color': pieces['H'][piece_type]['color']
                }

        # Posiciona Curiácios (base)
        start_row = 5
        for i, row in enumerate(formation):
            for j, piece_type in enumerate(row):
                self.board[start_row + i][start_col + j] = {
                    'team': 'C',
                    'type': piece_type,
                    'emoji': pieces['C'][piece_type]['emoji'],
                    'color': pieces['C'][piece_type]['color']
                }

def main():
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    # Botão de reinício
    if st.button("🔄 Reiniciar Jogo"):
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None
        st.rerun()
    
    # Inicializa o tabuleiro na sessão
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None
    
    # Cria o display do tabuleiro
    col1, _ = st.columns([4, 1])  # Removendo a última coluna
    
    with col1:
        for i in range(8):
            cols = st.columns(8)
            for j in range(8):
                with cols[j]:
                    # Cores do tabuleiro estilo xadrez
                    cell_color = '#DEB887' if (i + j) % 2 == 0 else '#8B4513'  # Marrom claro e escuro
                    piece = st.session_state.game_board.board[i][j]
                    
                    # Estilo CSS para as células
                    cell_style = f"""
                        <div style="
                            background-color: {cell_color};
                            width: 100%;
                            height: 50px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            border: 1px solid #666;
                            margin: 0;
                            padding: 0;
                        ">
                    """
                    
                    if piece:
                        button_style = f"""
                            color: {piece['color']};
                            font-size: 24px;
                            background: none;
                            border: none;
                            width: 100%;
                            height: 100%;
                            cursor: pointer;
                        """
                        
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

    # Informações sobre peça selecionada
    if st.session_state.selected_pos is not None:
        i, j = st.session_state.selected_pos
        piece = st.session_state.game_board.board[i][j]
        st.write("\nPeça selecionada:")
        st.markdown(f"<p style='color: {piece['color']};'>{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}</p>", unsafe_allow_html=True)
        if st.button("❌ Cancelar seleção"):
            st.session_state.selected_pos = None
            st.rerun()

if __name__ == "__main__":
    main()

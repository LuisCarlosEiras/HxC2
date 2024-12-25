import streamlit as st
import numpy as np

class GameBoard:
    def __init__(self):
        self.board_size_x = 7
        self.board_size_y = 8
        self.board = [[None for _ in range(self.board_size_x)] for _ in range(self.board_size_y)]
        self.setup_armies()
        self.selected_piece = None

    def setup_armies(self):
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

        formation_horatii = [
            ['A', 'A', 'A'],
            ['L', 'L', 'L'],
            ['S', 'S', 'S']
        ]

        formation_curiatii = [
            ['S', 'S', 'S'],
            ['L', 'L', 'L'],
            ['A', 'A', 'A']
        ]

        start_col = (self.board_size_x - 3) // 2

        # Posiciona Horácios (topo)
        for i, row in enumerate(formation_horatii):
            for j, piece_type in enumerate(row):
                self.board[i][start_col + j] = {
                    'team': 'H',
                    'type': piece_type,
                    'emoji': pieces['H'][piece_type]['emoji'],
                    'color': pieces['H'][piece_type]['color']
                }

        # Posiciona Curiácios (base)
        for i, row in enumerate(formation_curiatii):
            for j, piece_type in enumerate(row):
                self.board[5 + i][start_col + j] = {
                    'team': 'C',
                    'type': piece_type,
                    'emoji': pieces['C'][piece_type]['emoji'],
                    'color': pieces['C'][piece_type]['color']
                }
# -----------------------------
def main():
    st.title("Os Horácios e os Curiácios - Protótipo")

    # Estilos CSS atualizados para centralizar os guerreiros nas casas
    st.markdown("""
        <style>
            .board-wrapper {
                display: flex;
                align-items: center;
                margin: 20px 0;
            }
            .board-numbers {
                margin-right: 10px;
                text-align: right;
            }
            .board-letters {
                text-align: center;
                margin-top: 10px;
            }
            .cell {
                width: 60px;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                position: relative;
            }
            .white {
                background-color: #f0d9b5;
            }
            .black {
                background-color: #b58863;
            }
            .stButton {
                position: absolute;
                width: 100%;
                height: 100%;
            }
            .stButton > button {
                width: 100% !important;
                height: 100% !important;
                background: transparent !important;
                border: none !important;
                color: inherit !important;
                padding: 0 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            .stButton > button:hover {
                background: rgba(255, 255, 255, 0.2) !important;
            }
            .stButton > button:focus {
                box-shadow: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Resto do código permanece o mesmo...
# ------------------
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    col1, col2 = st.columns([3, 1])

    with col1:
        # Letras do tabuleiro (A-G)
        letters = "ABCDEFG"
        st.markdown('<div class="board-letters">' + 
                   ''.join([f'<span style="display:inline-block;width:60px">{letter}</span>' 
                           for letter in letters]) + '</div>', unsafe_allow_html=True)

        for i in range(8):
            cols = st.columns([0.2] + [1]*7)  # Uma coluna para números + 7 para o tabuleiro
            
            # Número da linha
            with cols[0]:
                st.markdown(f'<div style="text-align:right;padding-right:10px">{8-i}</div>', 
                          unsafe_allow_html=True)
            
            # Células do tabuleiro
            for j in range(7):
                with cols[j+1]:
                    cell_color = "white" if (i + j) % 2 == 0 else "black"
                    piece = st.session_state.game_board.board[i][j]

                    st.markdown(f'<div class="cell {cell_color}">', unsafe_allow_html=True)
                    
                    if piece:
                        if st.button(piece['emoji'], 
                                   key=f"cell_{i}_{j}",
                                   help=f"{'Horácio' if piece['team'] == 'H' else 'Curiácio'}"):
                            if st.session_state.selected_pos is None:
                                st.session_state.selected_pos = (i, j)
                            else:
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
                    else:
                        if st.button(" ", key=f"cell_{i}_{j}"):
                            if st.session_state.selected_pos is not None:
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.write("Legenda:")
        
        # Horácios (azul)
        st.markdown("<div style='color: #0000FF;'>Horácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("")
        
        # Curiácios (vermelho)
        st.markdown("<div style='color: #FF0000;'>Curiácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("")
        
        if st.session_state.selected_pos is not None:
            i, j = st.session_state.selected_pos
            piece = st.session_state.game_board.board[i][j]
            st.write("\nPeça selecionada:")
            st.markdown(f"<p style='color: {piece['color']};'>{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}</p>", 
                      unsafe_allow_html=True)
            if st.button("❌ Cancelar seleção"):
                st.session_state.selected_pos = None
                st.rerun()
        
        st.write("")
        
        if st.button("🔄 Reiniciar Jogo"):
            st.session_state.game_board = GameBoard()
            st.session_state.selected_pos = None
            st.rerun()

if __name__ == "__main__":
    main()

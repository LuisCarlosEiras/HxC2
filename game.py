import streamlit as st

class GameBoard:
    def __init__(self):
        self.board_size_x = 7
        self.board_size_y = 8
        self.board = [[None for _ in range(self.board_size_x)] for _ in range(self.board_size_y)]
        self.setup_armies()

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

def create_board_css():
    return """
    <style>
        .board {
            background: #333;
            padding: 10px;
            display: inline-block;
            border-radius: 4px;
        }
        .board-row {
            display: flex;
            align-items: center;
            height: 60px;
            margin: 0;
            padding: 0;
            font-size: 0; /* Remove espaço entre elementos inline */
        }
        .cell {
            width: 60px;
            height: 60px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            position: relative;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        .white {
            background-color: #f0d9b5;
        }
        .black {
            background-color: #b58863;
        }
        .coordinate {
            color: white;
            width: 30px;
            text-align: center;
            font-weight: bold;
            font-size: 16px; /* Restaura o tamanho da fonte para coordenadas */
        }
        .stButton > button {
            width: 60px !important;
            height: 60px !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            background: transparent !important;
            border: none !important;
            font-size: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        div[data-testid="column"] {
            padding: 0 !important;
            margin: 0 !important;
            font-size: 0; /* Remove espaço entre colunas */
        }
        /* Remove espaçamento entre linhas */
        div[data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
    </style>
    """
def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    st.markdown(create_board_css(), unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        # Início do tabuleiro
        st.markdown('<div class="board">', unsafe_allow_html=True)
        
        # Letras das colunas
        st.markdown('<div class="board-row"><div class="coordinate"></div>' + 
                   ''.join([f'<div class="coordinate">{chr(65+i)}</div>' for i in range(7)]) + 
                   '</div>', unsafe_allow_html=True)
        
        # Criar o tabuleiro
        for i in range(8):
            # Início da linha
            st.markdown(
                f'<div class="board-row">'
                f'<div class="coordinate">{8-i}</div>',
                unsafe_allow_html=True
            )
            
            # Células da linha
            cols = st.columns(7)
            for j, col in enumerate(cols):
                with col:
                    cell_color = "white" if (i + j) % 2 == 0 else "black"
                    st.markdown(f'<div class="cell {cell_color}">', unsafe_allow_html=True)
                    
                    piece = st.session_state.game_board.board[i][j]
                    if piece:
                        if st.button(piece['emoji'], key=f"cell_{i}_{j}"):
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
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.write("Legenda:")
        
        st.markdown("<div style='color: #0000FF;'>Horácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("")
        
        st.markdown("<div style='color: #FF0000;'>Curiácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        if st.session_state.selected_pos is not None:
            i, j = st.session_state.selected_pos
            piece = st.session_state.game_board.board[i][j]
            st.write("\nPeça selecionada:")
            st.markdown(
                f"<p style='color: {piece['color']};'>"
                f"{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}</p>",
                unsafe_allow_html=True
            )
            if st.button("❌ Cancelar seleção"):
                st.session_state.selected_pos = None
                st.rerun()
        
        if st.button("🔄 Reiniciar Jogo"):
            st.session_state.game_board = GameBoard()
            st.session_state.selected_pos = None
            st.rerun()

if __name__ == "__main__":
    main()

import streamlit as st

class GameBoard:
    def __init__(self):
        self.board_size_x = 7
        self.board_size_y = 8
        self.board = [[None for _ in range(self.board_size_x)] for _ in range(self.board_size_y)]
        self.setup_armies()

    def setup_armies(self):
        # Define as peças para cada exército
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

        # Formação inicial Horácios (topo)
        formation_horatii = [
            ['A', 'A', 'A'],  # Arqueiros
            ['L', 'L', 'L'],  # Lanceiros
            ['S', 'S', 'S']   # Espadachins
        ]

        # Formação inicial Curiácios (base)
        formation_curiatii = [
            ['S', 'S', 'S'],  # Espadachins
            ['L', 'L', 'L'],  # Lanceiros
            ['A', 'A', 'A']   # Arqueiros
        ]

        # Posiciona os exércitos
        formations = {
            'H': {'formation': formation_horatii, 'start_row': 0},
            'C': {'formation': formation_curiatii, 'start_row': 5}
        }

        # Coloca as peças no tabuleiro
        for army, data in formations.items():
            start_row = data['start_row']
            start_col = (self.board_size_x - 3) // 2
            
            for i, row in enumerate(data['formation']):
                for j, piece_type in enumerate(row):
                    self.board[start_row + i][start_col + j] = {
                        'team': army,
                        'type': piece_type,
                        'emoji': pieces[army][piece_type]['emoji'],
                        'color': pieces[army][piece_type]['color']
                    }

def create_board_css():
    return """
    <style>
        .board-container {
            background: #333;
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .white-cell {
            background-color: #f0d9b5;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .black-cell {
            background-color: #b58863;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .coordinate {
            color: white;
            font-weight: bold;
            padding: 5px;
            text-align: center;
        }
        .stButton > button {
            width: 60px !important;
            height: 60px !important;
            background: transparent !important;
            border: none !important;
            font-size: 2em !important;
            padding: 0 !important;
            line-height: 60px !important;
        }
        .stButton > button:hover {
            background: rgba(255, 255, 0, 0.2) !important;
        }
    </style>
    """

def create_cell(i, j, piece=None):
    cell_color = "white-cell" if (i + j) % 2 == 0 else "black-cell"
    return f'<div class="{cell_color}">'

def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    st.markdown(create_board_css(), unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        # Cria o container do tabuleiro
        st.markdown('<div class="board-container">', unsafe_allow_html=True)
        
        # Letras das colunas (A-G)
        cols = st.columns(8)  # Extra column for row numbers
        for j in range(7):
            with cols[j+1]:
                st.markdown(f'<div class="coordinate">{chr(65+j)}</div>', unsafe_allow_html=True)
        
        # Tabuleiro
        for i in range(8):
            cols = st.columns(8)  # Include column for row numbers
            
            # Número da linha
            with cols[0]:
                st.markdown(f'<div class="coordinate">{8-i}</div>', unsafe_allow_html=True)
            
            # Células do tabuleiro
            for j in range(7):
                with cols[j+1]:
                    piece = st.session_state.game_board.board[i][j]
                    st.markdown(create_cell(i, j), unsafe_allow_html=True)
                    
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

    with col2:
        st.write("Legenda:")
        
        # Horácios (azul)
        st.markdown("<div style='color: #0000FF; margin-bottom: 10px;'>Horácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("")
        
        # Curiácios (vermelho)
        st.markdown("<div style='color: #FF0000; margin-bottom: 10px;'>Curiácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("")
        
        # Informação da peça selecionada
        if st.session_state.selected_pos is not None:
            i, j = st.session_state.selected_pos
            piece = st.session_state.game_board.board[i][j]
            st.write("\nPeça selecionada:")
            st.markdown(
                f"<p style='color: {piece['color']};'>{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}</p>",
                unsafe_allow_html=True
            )
            if st.button("❌ Cancelar seleção"):
                st.session_state.selected_pos = None
                st.rerun()
        
        st.write("")
        
        # Botão de reinício
        if st.button("🔄 Reiniciar Jogo"):
            st.session_state.game_board = GameBoard()
            st.session_state.selected_pos = None
            st.rerun()

if __name__ == "__main__":
    main()

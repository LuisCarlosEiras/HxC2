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

        for army, formation, start_row in [('H', formation_horatii, 0), ('C', formation_curiatii, 5)]:
            start_col = (self.board_size_x - 3) // 2
            for i, row in enumerate(formation):
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
        .chess-board {
            border-collapse: collapse;
            background: #333;
            padding: 10px;
            margin: auto;
        }
        .chess-board td {
            width: 60px;
            height: 60px;
            text-align: center;
            vertical-align: middle;
            padding: 0;
        }
        .white-cell {
            background-color: #f0d9b5;
        }
        .black-cell {
            background-color: #b58863;
        }
        .coordinate {
            color: white;
            font-weight: bold;
            padding: 5px;
        }
        .stButton {
            height: 60px;
            width: 60px;
            padding: 0 !important;
            margin: 0 !important;
        }
        .stButton > button {
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            border: none !important;
            background: transparent !important;
            font-size: 35px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div[data-testid="column"] {
            padding: 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }
        td {
            position: relative;
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
        # Criar o tabuleiro como uma tabela HTML
        table_html = '<table class="chess-board"><tr><td></td>'
        
        # Adicionar letras das colunas
        for j in range(7):
            table_html += f'<td class="coordinate">{chr(65+j)}</td>'
        table_html += '</tr>'
        
        st.markdown(table_html, unsafe_allow_html=True)

        # Criar o tabuleiro linha por linha
        for i in range(8):
            cols = st.columns([0.5] + [1]*7)
            
            # Número da linha
            with cols[0]:
                st.markdown(f'<div class="coordinate">{8-i}</div>', unsafe_allow_html=True)
            
            # Células do tabuleiro
            for j in range(7):
                with cols[j+1]:
                    cell_color = "white-cell" if (i + j) % 2 == 0 else "black-cell"
                    st.markdown(f'<div class="{cell_color}">', unsafe_allow_html=True)
                    
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

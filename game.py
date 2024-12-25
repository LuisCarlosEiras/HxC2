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

def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")

    # CSS aprimorado para garantir que os guerreiros fiquem dentro das células
    st.markdown("""
    <style>
        .board {
            display: table;
            border-collapse: collapse;
            background: #333;
            padding: 10px;
            margin: 0 auto;
        }
        .row {
            display: table-row;
        }
        .cell {
            display: table-cell;
            width: 60px;
            height: 60px;
            text-align: center;
            vertical-align: middle;
            position: relative;
        }
        .white {
            background-color: #f0d9b5;
        }
        .black {
            background-color: #b58863;
        }
        .coordinate {
            color: white;
            padding: 5px;
            text-align: center;
        }
        .stButton {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        .stButton > button {
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            font-size: 30px !important;
            line-height: 60px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        .piece-blue { color: #0000FF; }
        .piece-red { color: #FF0000; }
        div[data-testid="column"] {
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    col1, col2 = st.columns([3, 1])

    with col1:
        # Tabuleiro HTML base
        board_html = '<div class="board">'
        
        # Linha de letras
        board_html += '<div class="row"><div class="cell coordinate"></div>'
        for j in range(7):
            board_html += f'<div class="cell coordinate">{chr(65+j)}</div>'
        board_html += '</div>'

        # Linhas do tabuleiro
        for i in range(8):
            board_html += f'<div class="row"><div class="cell coordinate">{8-i}</div>'
            
            # Células da linha
            for j in range(7):
                cell_color = "white" if (i + j) % 2 == 0 else "black"
                board_html += f'<div class="cell {cell_color}"></div>'
            board_html += '</div>'
        board_html += '</div>'
        
        st.markdown(board_html, unsafe_allow_html=True)

        # Botões para interação
        for i in range(8):
            cols = st.columns([0.5] + [1]*7)
            for j in range(7):
                with cols[j+1]:
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

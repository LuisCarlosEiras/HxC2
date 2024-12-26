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
                'S': {'emoji': '⚔️', 'color': 'blue'},
                'L': {'emoji': '🗡️', 'color': 'blue'},
                'A': {'emoji': '🏹', 'color': 'blue'}
            },
            'C': {  # Curiácios (vermelho)
                'S': {'emoji': '⚔️', 'color': 'red'},
                'L': {'emoji': '🗡️', 'color': 'red'},
                'A': {'emoji': '🏹', 'color': 'red'}
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

def create_board_html(board):
    css = """
    <style>
        .board-container {
            display: inline-block;
            padding: 5px;
            background: #333;
            border-radius: 4px;
            margin: auto;
            text-align: center;
        }
        table.chess-board {
            border-collapse: collapse;
            border-spacing: 0;
            margin: 0 auto;
            padding: 0;
        }
        .chess-board th, .chess-board td {
            width: 40px;
            height: 40px;
            padding: 0;
            margin: 0;
            text-align: center;
            vertical-align: middle;
            border: 1px solid #333;
        }
        .chess-board th {
            color: white;
            font-size: 12px;
            padding: 5px;
        }
        .white-cell {
            background-color: #f0d9b5;
        }
        .black-cell {
            background-color: #b58863;
        }
        .piece {
            font-size: 25px;
            line-height: 40px;
            margin: 0;
            padding: 0;
        }
        .button-cell {
            width: 40px;
            height: 40px;
            padding: 0;
            margin: 0;
            border: none;
            background: transparent;
            cursor: pointer;
        }
    </style>
    """

    html = css + '<div class="board-container"><table class="chess-board">'
    
    # Adiciona cabeçalho com letras
    html += '<tr><th></th>'
    for col in range(7):
        html += f'<th>{chr(65 + col)}</th>'
    html += '</tr>'
    
    # Adiciona linhas do tabuleiro
    for row in range(8):
        html += f'<tr><th>{8 - row}</th>'
        for col in range(7):
            cell_color = 'white-cell' if (row + col) % 2 == 0 else 'black-cell'
            piece = board[row][col]
            piece_html = f'<div class="piece" style="color: {piece["color"]};">{piece["emoji"]}</div>' if piece else ''
            html += f'<td class="{cell_color}">{piece_html}</td>'
        html += '</tr>'
    html += '</table></div>'
    
    return html

def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    col1, col2 = st.columns([2, 1])

    with col1:
        # Renderiza o tabuleiro
        st.markdown(create_board_html(st.session_state.game_board.board), unsafe_allow_html=True)
        
        # Matriz de botões invisíveis para controle
        cols = st.columns(7)
        for i in range(8):
            for j in range(7):
                with cols[j]:
                    if st.button("", key=f"btn_{i}_{j}", help=f"Posição {chr(65+j)}{8-i}"):
                        if st.session_state.selected_pos is None and st.session_state.game_board.board[i][j]:
                            st.session_state.selected_pos = (i, j)
                        elif st.session_state.selected_pos is not None:
                            old_i, old_j = st.session_state.selected_pos
                            st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                            st.session_state.game_board.board[old_i][old_j] = None
                            st.session_state.selected_pos = None
                        st.rerun()

    with col2:
        st.write("Legenda:")
        st.markdown("<div style='color: blue;'>Horácios:</div>", unsafe_allow_html=True)
        st.write("⚔️ - Espadachim")
        st.write("🗡️ - Lanceiro")
        st.write("🏹 - Arqueiro")
        
        st.write("")
        
        st.markdown("<div style='color: red;'>Curiácios:</div>", unsafe_allow_html=True)
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

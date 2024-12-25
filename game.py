import streamlit as st

class GameBoard:
    def __init__(self):
        self.board_size_x = 7
        self.board_size_y = 8
        self.board = [[None for _ in range(self.board_size_x)] for _ in range(self.board_size_y)]
        self.setup_armies()

    def setup_armies(self):
        # Define as peças para cada exército
        armies = {
            'H': {  # Horácios (azul)
                'pieces': [
                    ['A', 'A', 'A'],  # Arqueiros
                    ['L', 'L', 'L'],  # Lanceiros
                    ['S', 'S', 'S']   # Espadachins
                ],
                'start_row': 0,
                'color': '#0000FF'
            },
            'C': {  # Curiácios (vermelho)
                'pieces': [
                    ['S', 'S', 'S'],  # Espadachins
                    ['L', 'L', 'L'],  # Lanceiros
                    ['A', 'A', 'A']   # Arqueiros
                ],
                'start_row': 5,
                'color': '#FF0000'
            }
        }

        # Mapeia tipos de peças para emojis
        piece_emojis = {
            'S': '⚔️',  # Espadachim
            'L': '🗡️',  # Lanceiro
            'A': '🏹'   # Arqueiro
        }

        # Posiciona as peças
        for army, data in armies.items():
            start_row = data['start_row']
            start_col = (self.board_size_x - 3) // 2
            
            for i, row in enumerate(data['pieces']):
                for j, piece_type in enumerate(row):
                    self.board[start_row + i][start_col + j] = {
                        'team': army,
                        'type': piece_type,
                        'emoji': piece_emojis[piece_type],
                        'color': data['color']
                    }

def create_board_css():
    return """
    <style>
        .chess-board {
            border-collapse: collapse;
            border: 2px solid #333;
            background: #333;
            margin: 20px auto;
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
            text-align: center;
        }
        .stButton > button {
            width: 100%;
            height: 100%;
            padding: 0 !important;
            font-size: 2em !important;
            line-height: 60px !important;
            border: none !important;
            background: transparent !important;
            color: inherit;
        }
        .piece-blue {
            color: #0000FF !important;
        }
        .piece-red {
            color: #FF0000 !important;
        }
    </style>
    """

def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    # Inicializa o estado do jogo
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    # Injeta CSS
    st.markdown(create_board_css(), unsafe_allow_html=True)

    # Layout principal
    col1, col2 = st.columns([3, 1])

    with col1:
        # Cria o tabuleiro como uma tabela HTML
        board_html = '<table class="chess-board"><tr><td></td>'
        
        # Adiciona letras das colunas
        for col in range(7):
            board_html += f'<td class="coordinate">{chr(65 + col)}</td>'
        board_html += '</tr>'

        # Cria as linhas do tabuleiro
        for i in range(8):
            board_html += f'<tr><td class="coordinate">{8-i}</td>'
            
            for j in range(7):
                cell_color = "white-cell" if (i + j) % 2 == 0 else "black-cell"
                board_html += f'<td class="{cell_color}">'
                
                piece = st.session_state.game_board.board[i][j]
                if piece:
                    color_class = "piece-blue" if piece['team'] == 'H' else "piece-red"
                    board_html += f'<div class="{color_class}">{piece["emoji"]}</div>'
                board_html += '</td>'
            
            board_html += '</tr>'
        
        board_html += '</table>'
        st.markdown(board_html, unsafe_allow_html=True)

        # Matriz de botões transparentes sobre o tabuleiro
        for i in range(8):
            cols = st.columns(7)
            for j, col in enumerate(cols):
                with col:
                    piece = st.session_state.game_board.board[i][j]
                    if piece:
                        if st.button('', key=f'cell_{i}_{j}'):
                            if st.session_state.selected_pos is None:
                                st.session_state.selected_pos = (i, j)
                            else:
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()
                    else:
                        if st.button('', key=f'empty_{i}_{j}'):
                            if st.session_state.selected_pos is not None:
                                old_i, old_j = st.session_state.selected_pos
                                st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
                                st.session_state.game_board.board[old_i][old_j] = None
                                st.session_state.selected_pos = None
                                st.rerun()

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
        
        st.write("")
        
        if st.button("🔄 Reiniciar Jogo"):
            st.session_state.game_board = GameBoard()
            st.session_state.selected_pos = None
            st.rerun()

if __name__ == "__main__":
    main()

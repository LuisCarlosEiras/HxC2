import streamlit as st
import altair as alt
import pandas as pd

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

def create_board_html(board):
    css = """
    <style>
        .board-container {
            background: #333;
            padding: 10px;
            display: inline-block;
            border-radius: 4px;
        }
        table.chess-board {
            border-collapse: collapse;
            border-spacing: 0;
            margin: 0;
            padding: 0;
        }
        .chess-board th, .chess-board td {
            width: 60px;
            height: 60px;
            padding: 0;
            margin: 0;
            text-align: center;
            vertical-align: middle;
            border: none;
        }
        .chess-board th {
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        .white-cell {
            background-color: #f0d9b5;
        }
        .black-cell {
            background-color: #b58863;
        }
        .piece-button {
            width: 100%;
            height: 100%;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 40px;
            padding: 0;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
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
            if piece:
                button_html = f'<button class="piece-button" id="btn_{row}_{col}" onclick="handleClick({row}, {col})">{piece["emoji"]}</button>'
            else:
                button_html = '<button class="piece-button" id="btn_{row}_{col}" onclick="handleClick({row}, {col})"></button>'
            html += f'<td class="{cell_color}">{button_html}</td>'
        html += '</tr>'
    html += '</table></div>'
    
    return html

def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")
    
    if 'game_board' not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.selected_pos = None

    col1, col2 = st.columns([3, 1])

    with col1:
        # Renderiza o tabuleiro base
        st.markdown(create_board_html(st.session_state.game_board.board), unsafe_allow_html=True)
        
        # Crie um DataFrame para representar o tabuleiro
        df = pd.DataFrame({
            'x': range(7),
            'y': range(8),
            'piece': [None] * 56
        })

        # Adicione as peças ao DataFrame
        for i in range(8):
            for j in range(7):
                piece = st.session_state.game_board.board[i][j]
                if piece:
                    df.loc[(i, j), 'piece'] = piece['emoji']

        # Crie um gráfico com o tabuleiro
        chart = alt.Chart(df).mark_square().encode(
            x='x',
            y='y',
            color='piece'
        )

        # Adicione um evento de clique ao gráfico
        chart.on('click', handle_click)

        # Renderize o gráfico
        st.altair_chart(chart, use_container_width=True)

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

def handle_click(i, j):
    if st.session_state.selected_pos is not None:
        old_i, old_j = st.session_state.selected_pos
        st.session_state.game_board.board[i][j] = st.session_state.game_board.board[old_i][old_j]
        st.session_state.game_board.board[old_i][old_j] = None
        st.session_state.selected_pos = None
        st.rerun()

if __name__ == "__main__":
    main()

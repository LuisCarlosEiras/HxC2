import streamlit as st
from PIL import Image, ImageDraw, ImageFont

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

    def draw_board(self):
        cell_size = 60
        board_img = Image.new('RGB', (self.board_size_x * cell_size, self.board_size_y * cell_size), (255, 255, 255))
        draw = ImageDraw.Draw(board_img)

        for i in range(self.board_size_y):
            for j in range(self.board_size_x):
                color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
                draw.rectangle([j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size], fill=color)
                piece = self.board[i][j]
                if piece:
                    font = ImageFont.load_default()
                    draw.text((j * cell_size + 20, i * cell_size + 20), piece['emoji'], fill=piece['color'], font=font)

        return board_img

def main():
    st.set_page_config(layout="wide")
    st.title("Os Horácios e os Curiácios - Protótipo")

    if 'game_board' not in st.session_state:
        st.session_state['game_board'] = GameBoard()
        st.session_state['selected_pos'] = None

    game_board = st.session_state['game_board']
    img = game_board.draw_board()

    # Show the image in Streamlit
    st.image(img, caption=None, use_column_width=True)

    # Handle clicks
    click_info = st.experimental_get_query_params()
    if 'click_pos' in click_info:
        row, col = map(int, click_info['click_pos'][0].split(','))
        if st.session_state['selected_pos'] is None:
            st.session_state['selected_pos'] = (row, col)
        else:
            old_row, old_col = st.session_state['selected_pos']
            st.session_state['game_board'].board[row][col] = st.session_state['game_board'].board[old_row][old_col]
            st.session_state['game_board'].board[old_row][old_col] = None
            st.session_state['selected_pos'] = None
            del click_info['click_pos']
            st.experimental_rerun()

    # Display legend
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

    if st.session_state['selected_pos'] is not None:
        i, j = st.session_state['selected_pos']
        piece = st.session_state['game_board'].board[i][j]
        st.write("\nPeça selecionada:")
        st.markdown(
            f"<p style='color: {piece['color']};'>"
            f"{'Horácio' if piece['team'] == 'H' else 'Curiácio'} {piece['emoji']}</p>",
            unsafe_allow_html=True
        )
        if st.button("❌ Cancelar seleção"):
            st.session_state['selected_pos'] = None

    if st.button("🔄 Reiniciar Jogo"):
        st.session_state['game_board'] = GameBoard()
        st.session_state['selected_pos'] = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()

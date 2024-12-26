import streamlit as st
import numpy as np
import cv2

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

    def draw_board(self):
        img = np.zeros((480, 420, 3), dtype=np.uint8)
        img.fill(255)
        for i in range(8):
            for j in range(7):
                color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
                cv2.rectangle(img, (j * 60, i * 60), ((j + 1) * 60, (i + 1) * 60), color, -1)
                piece = self.board[i][j]
                if piece:
                    cv2.putText(img, piece['emoji'], (j * 60 + 15, i * 60 + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        return img

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        col = x // 60
        row = y // 60
        if 0 <= col < 7 and 0 <= row < 8:
            st.session_state['click_pos'] = (row, col)

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

    # Bind the click event
    cv2.namedWindow('Board')
    cv2.setMouseCallback('Board', click_event)

    # Handle clicks
    if 'click_pos' in st.session_state:
        row, col = st.session_state['click_pos']
        if st.session_state['selected_pos'] is None:
            st.session_state['selected_pos'] = (row, col)
        else:
            old_row, old_col = st.session_state['selected_pos']
            st.session_state['game_board'].board[row][col] = st.session_state['game_board'].board[old_row][old_col]
            st.session_state['game_board'].board[old_row][old_col] = None
            st.session_state['selected_pos'] = None
            del st.session_state['click_pos']
            st.experimental_rerun()

    # Display legend
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

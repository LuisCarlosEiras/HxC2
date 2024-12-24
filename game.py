import streamlit as st
import numpy as np
from enum import Enum
import random

class PieceType(Enum):
    EMPTY = 0
    ARCHER = 1
    SPEARMAN = 2
    SWORDSMAN = 3

class Army(Enum):
    NONE = 0
    HORATII = 1
    CURIATII = 2

class Piece:
    def __init__(self, piece_type, army):
        self.piece_type = piece_type
        self.army = army
        if piece_type == PieceType.ARCHER:
            self.weapons = 3
            self.movement_range = 1
        elif piece_type == PieceType.SPEARMAN:
            self.weapons = 3
            self.movement_range = 2
        elif piece_type == PieceType.SWORDSMAN:
            self.weapons = 1
            self.movement_range = 2
        else:
            self.weapons = 0
            self.movement_range = 0

class GameState:
    def __init__(self):
        self.board = [[Piece(PieceType.EMPTY, Army.NONE) for _ in range(18)] for _ in range(9)]
        self.current_turn = Army.HORATII
        self.selected_piece = None
        self.valid_moves = []
        self.initialize_board()
    
    def initialize_board(self):
        piece_types = [
            [PieceType.ARCHER, PieceType.ARCHER, PieceType.ARCHER],
            [PieceType.SPEARMAN, PieceType.SPEARMAN, PieceType.SPEARMAN],
            [PieceType.SWORDSMAN, PieceType.SWORDSMAN, PieceType.SWORDSMAN]
        ]
        
        for i in range(3):
            for j in range(3):
                self.board[i][7+j] = Piece(piece_types[i][j], Army.HORATII)
                self.board[6+i][7+j] = Piece(piece_types[2-i][j], Army.CURIATII)

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        valid_moves = []
        
        if piece.piece_type == PieceType.EMPTY:
            return []

        movement_range = piece.movement_range
        
        for dx in range(-movement_range, movement_range + 1):
            for dy in range(-movement_range, movement_range + 1):
                new_row = row + dx
                new_col = col + dy
                
                if (0 <= new_row < 9 and 0 <= new_col < 18 and
                    (dx != 0 or dy != 0) and
                    abs(dx) + abs(dy) <= movement_range):
                    
                    target = self.board[new_row][new_col]
                    if (target.piece_type == PieceType.EMPTY or 
                        target.army != piece.army):
                        valid_moves.append((new_row, new_col))
        
        return valid_moves

    def move_piece(self, from_pos, to_pos):
        if to_pos in self.valid_moves:
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = Piece(PieceType.EMPTY, Army.NONE)
            
            self.current_turn = Army.CURIATII if self.current_turn == Army.HORATII else Army.HORATII
            
            self.selected_piece = None
            self.valid_moves = []
            return True
        return False

def get_piece_symbol(piece):
    if piece.piece_type == PieceType.EMPTY:
        return " "
    elif piece.piece_type == PieceType.ARCHER:
        return "🏹"
    elif piece.piece_type == PieceType.SPEARMAN:
        return "🗡️"
    elif piece.piece_type == PieceType.SWORDSMAN:
        return "⚔️"
    return " "

def main():
    st.title("Os Horácios e os Curiácios")
    
    if 'game_state' not in st.session_state:
        st.session_state.game_state = GameState()
    
    game_state = st.session_state.game_state

    # Container para o tabuleiro com estilo CSS personalizado
    board_container = st.container()
    
    with board_container:
        for i in range(9):
            cols = st.columns(18)
            for j in range(18):
                piece = game_state.board[i][j]
                
                # Cor do tabuleiro de xadrez
                is_dark = (i + j) % 2 == 0
                base_color = '#769656' if is_dark else '#eeeed2'  # Cores de xadrez tradicional
                
                # Destacar casas válidas para movimento
                if (i, j) in game_state.valid_moves:
                    bg_color = '#baca44'  # Verde mais claro para movimentos válidos
                elif game_state.selected_piece == (i, j):
                    bg_color = '#f6f669'  # Amarelo para peça selecionada
                else:
                    bg_color = base_color
                
                # Cor do texto baseada no exército
                if piece.army == Army.HORATII:
                    text_color = "#0000FF"  # Azul
                elif piece.army == Army.CURIATII:
                    text_color = "#FF0000"  # Vermelho
                else:
                    text_color = "#000000"  # Preto
                
                # Símbolo da peça
                symbol = get_piece_symbol(piece)
                
                # Criar botão com estilo personalizado
                button_style = f"""
                    <div style="
                        background-color: {bg_color};
                        color: {text_color};
                        width: 40px;
                        height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        border: 1px solid #666;
                        cursor: pointer;
                    ">
                        {symbol}
                    </div>
                """
                
                if cols[j].button(
                    symbol,
                    key=f"{i}-{j}",
                    help=f"Posição ({i},{j})",
                    use_container_width=True
                ):
                    if (game_state.selected_piece is None and 
                        piece.piece_type != PieceType.EMPTY and 
                        piece.army == game_state.current_turn):
                        game_state.selected_piece = (i, j)
                        game_state.valid_moves = game_state.get_valid_moves(i, j)
                        st.rerun()
                    elif game_state.selected_piece is not None:
                        if game_state.move_piece(game_state.selected_piece, (i, j)):
                            st.rerun()
                        else:
                            game_state.selected_piece = None
                            game_state.valid_moves = []
                            st.rerun()

    # Informações do jogo
    st.write(f"Turno atual: {'Horácios' if game_state.current_turn == Army.HORATII else 'Curiácios'}")
    
    if st.button("Reiniciar Jogo"):
        st.session_state.game_state = GameState()
        st.rerun()

if __name__ == "__main__":
    main()

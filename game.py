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
        
        # Verificar todas as direções possíveis
        for dx in range(-movement_range, movement_range + 1):
            for dy in range(-movement_range, movement_range + 1):
                new_row = row + dx
                new_col = col + dy
                
                # Verificar se o movimento está dentro do tabuleiro
                if (0 <= new_row < 9 and 0 <= new_col < 18 and
                    (dx != 0 or dy != 0) and  # não permanecer na mesma posição
                    abs(dx) + abs(dy) <= movement_range):  # respeitar o alcance do movimento
                    
                    # Verificar se a casa está vazia ou tem um inimigo
                    target = self.board[new_row][new_col]
                    if (target.piece_type == PieceType.EMPTY or 
                        target.army != piece.army):
                        valid_moves.append((new_row, new_col))
        
        return valid_moves

    def move_piece(self, from_pos, to_pos):
        if to_pos in self.valid_moves:
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Realizar o movimento
            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = Piece(PieceType.EMPTY, Army.NONE)
            
            # Trocar o turno
            self.current_turn = Army.CURIATII if self.current_turn == Army.HORATII else Army.HORATII
            
            # Limpar seleção
            self.selected_piece = None
            self.valid_moves = []
            return True
        return False

def main():
    st.title("Os Horácios e os Curiácios")
    
    if 'game_state' not in st.session_state:
        st.session_state.game_state = GameState()
    
    game_state = st.session_state.game_state
    
    # Criar o tabuleiro visual
    for i in range(9):
        cols = st.columns(18)
        for j in range(18):
            piece = game_state.board[i][j]
            bg_color = '#4f4f4f' if (i + j) % 2 == 0 else '#8f8f8f'
            
            # Destacar casas válidas para movimento
            if (i, j) in game_state.valid_moves:
                bg_color = '#90EE90'  # Verde claro para movimentos válidos
            
            # Destacar peça selecionada
            if game_state.selected_piece == (i, j):
                bg_color = '#FFD700'  # Dourado para peça selecionada
            
            if piece.piece_type == PieceType.EMPTY:
                symbol = " "
            else:
                symbols = {
                    PieceType.ARCHER: "🏹",
                    PieceType.SPEARMAN: "🗡️",
                    PieceType.SWORDSMAN: "⚔️"
                }
                symbol = symbols[piece.piece_type]
            
            if piece.army == Army.HORATII:
                color = "blue"
            elif piece.army == Army.CURIATII:
                color = "red"
            else:
                color = "white"
            
            # Criar botão clicável para cada célula
            if cols[j].button(symbol, key=f"{i}-{j}", help=f"Posição ({i},{j})"):
                # Se não há peça selecionada e a célula tem uma peça do jogador atual
                if (game_state.selected_piece is None and 
                    piece.piece_type != PieceType.EMPTY and 
                    piece.army == game_state.current_turn):
                    game_state.selected_piece = (i, j)
                    game_state.valid_moves = game_state.get_valid_moves(i, j)
                
                # Se há uma peça selecionada, tentar mover para a nova posição
                elif game_state.selected_piece is not None:
                    from_pos = game_state.selected_piece
                    to_pos = (i, j)
                    if game_state.move_piece(from_pos, to_pos):
                        st.rerun()
                    else:
                        # Se o movimento for inválido, limpar seleção
                        game_state.selected_piece = None
                        game_state.valid_moves = []
                        st.rerun()
    
    # Mostrar o turno atual
    st.write(f"Turno atual: {'Horácios' if game_state.current_turn == Army.HORATII else 'Curiácios'}")
    
    # Adicionar botão de reiniciar jogo
    if st.button("Reiniciar Jogo"):
        st.session_state.game_state = GameState()
        st.rerun()

if __name__ == "__main__":
    main()

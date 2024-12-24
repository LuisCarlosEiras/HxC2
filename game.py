# game.py
import streamlit as st
import numpy as np
from enum import Enum
import random

# Enums para os tipos de peças e exércitos
class PieceType(Enum):
    EMPTY = 0
    ARCHER = 1
    SPEARMAN = 2
    SWORDSMAN = 3

class Army(Enum):
    NONE = 0
    HORATII = 1
    CURIATII = 2

# Classe para representar uma peça no tabuleiro
class Piece:
    def __init__(self, piece_type, army):
        self.piece_type = piece_type
        self.army = army
        # Definir quantidade inicial de armas
        if piece_type == PieceType.ARCHER:
            self.weapons = 3  # flechas
        elif piece_type == PieceType.SPEARMAN:
            self.weapons = 3  # lanças
        elif piece_type == PieceType.SWORDSMAN:
            self.weapons = 1  # espada
        else:
            self.weapons = 0

class GameState:
    def __init__(self):
        # Alterado para 18 x 9
        self.board = [[Piece(PieceType.EMPTY, Army.NONE) for _ in range(9)] for _ in range(18)]
        self.current_turn = Army.HORATII
        self.initialize_board()
    
    def initialize_board(self):
        # Configuração inicial dos exércitos
        piece_types = [
            [PieceType.ARCHER, PieceType.ARCHER, PieceType.ARCHER],
            [PieceType.SPEARMAN, PieceType.SPEARMAN, PieceType.SPEARMAN],
            [PieceType.SWORDSMAN, PieceType.SWORDSMAN, PieceType.SWORDSMAN]
        ]
        
        # Posicionar Horácios (lado esquerdo)
        for i in range(3):
            for j in range(3):
                self.board[7+i][0+j] = Piece(piece_types[i][j], Army.HORATII)
        
        # Posicionar Curiácios (lado direito)
        for i in range(3):
            for j in range(3):
                self.board[7+i][6-j] = Piece(piece_types[i][j], Army.CURIATII)

# Interface Streamlit
def main():
    st.title("Os Horácios e os Curiácios")
    
    # Inicializar o estado do jogo
    if 'game_state' not in st.session_state:
        st.session_state.game_state = GameState()
    
    # Exibir o tabuleiro
    game_state = st.session_state.game_state
    
    # Criar o tabuleiro visual
    for i in range(18):  # linhas
        cols = st.columns(9)  # colunas
        for j in range(9):
            piece = game_state.board[i][j]
            # Definir a cor da célula (alternando cores como num tabuleiro de xadrez)
            bg_color = '#4f4f4f' if (i + j) % 2 == 0 else '#8f8f8f'
            
            # Definir o símbolo da peça
            if piece.piece_type == PieceType.EMPTY:
                symbol = " "
            else:
                symbols = {
                    PieceType.ARCHER: "🏹",
                    PieceType.SPEARMAN: "🗡️",
                    PieceType.SWORDSMAN: "⚔️"
                }
                symbol = symbols[piece.piece_type]
            
            # Adicionar cor ao exército
            if piece.army == Army.HORATII:
                color = "blue"
            elif piece.army == Army.CURIATII:
                color = "red"
            else:
                color = "white"
                
            cols[j].markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    color: {color};
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                    margin: 0;
                    padding: 0;
                ">
                    {symbol}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Mostrar o turno atual
    st.write(f"Turno atual: {'Horácios' if game_state.current_turn == Army.HORATII else 'Curiácios'}")

if __name__ == "__main__":
    main()

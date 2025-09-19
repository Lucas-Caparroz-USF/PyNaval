# jogador.py
# Classe Jogador

from .tabuleiro import Tabuleiro
from .navio import Navio
import random

class Jogador:
    def __init__(self):
        self.tabuleiro = Tabuleiro()  # Cria tabuleiro
        self.navios = []  # Lista de navios do jogador

    def posicionar_navios_automatico(self):
        """
        Posiciona automaticamente 5 navios no tabuleiro
        """
        tamanhos = [5,4,3,3,2]
        for t in tamanhos:
            colocado = False
            while not colocado:
                navio = Navio(t)
                linha = random.randint(0,9)
                coluna = random.randint(0,9)
                orientacao = random.choice(['H','V'])
                colocado = self.tabuleiro.posicionar_navio(navio, linha, coluna, orientacao)
                if colocado:
                    self.navios.append(navio)

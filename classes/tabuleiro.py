# tabuleiro.py
# Classe do Tabuleiro e função para desenhar

import pygame

class Tabuleiro:
    def __init__(self, tamanho=10):
        self.tamanho = tamanho  # Tabuleiro 10x10
        # Inicializa grid: cada célula é um dicionário
        self.grid = [[{'navio': None, 'atingido': False} for _ in range(tamanho)] for _ in range(tamanho)]

    def posicionar_navio(self, navio, linha, coluna, orientacao):
        """
        Posiciona navio na grid.
        orientacao = 'H' ou 'V'
        """
        celulas = []
        for i in range(navio.tamanho):
            li = linha + i if orientacao == 'V' else linha
            co = coluna + i if orientacao == 'H' else coluna
            if li >= self.tamanho or co >= self.tamanho:
                return False  # Não cabe no tabuleiro
            if self.grid[li][co]['navio'] is not None:
                return False  # Já existe navio nesta posição
            celulas.append((li, co))
        # Posiciona navio
        for li, co in celulas:
            self.grid[li][co]['navio'] = navio
        navio.celulas = celulas
        return True

    def receber_tiro(self, linha, coluna):
        """
        Marca ataque em uma célula.
        Retorna: "acertou", "agua", "afundou", "repetido"
        """
        celula = self.grid[linha][coluna]
        if celula['atingido']:
            return "repetido"  # Já foi atacada
        celula['atingido'] = True
        if celula['navio'] is None:
            return "agua"
        navio = celula['navio']
        navio.atingidos += 1
        if navio.afundado():
            return "afundou"
        return "acertou"

def desenhar_tabuleiro(tela, tabuleiro, pos_x, pos_y, mostrar_navios=False):
    """
    Desenha o tabuleiro na tela.
    """
    CELULA = 40
    for i in range(tabuleiro.tamanho):
        for j in range(tabuleiro.tamanho):
            celula = tabuleiro.grid[i][j]
            cor = (0, 102, 204)  # Azul água
            if mostrar_navios and celula['navio'] is not None:
                cor = (128,128,128)  # Cinza navio
            if celula['atingido']:
                cor = (255,0,0) if celula['navio'] else (255,255,255)
            ret = pygame.Rect(pos_x + j*CELULA, pos_y + i*CELULA, CELULA, CELULA)
            pygame.draw.rect(tela, cor, ret)
            pygame.draw.rect(tela, (0,0,0), ret, 1)

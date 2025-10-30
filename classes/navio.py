# navio.py
# Define a classe Navio

class Navio:
    def __init__(self, tamanho):
        self.tamanho = tamanho  # Quantas células o navio ocupa
        self.atingidos = 0      # Contador de acertos
        self.celulas = []       # Lista de posições do navio (linha, coluna)
    
    def afundado(self):
        # Retorna True se todos os quadrados foram atingidos
        return self.atingidos >= self.tamanho

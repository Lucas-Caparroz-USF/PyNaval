class Navio:  # Cria a classe Navio
    def __init__(self, tamanho, nome):  # Construtor da classe
        self.tamanho = tamanho          # Define quantas casas o navio ocupa
        self.nome = nome                # Nome do navio (porta-aviões, encouraçado...)
        self.posicoes = []              # Lista de posições do navio
        self.afundado = False           # Status do navio: afundado ou não

    def verificar_afundado(self):  # Verifica se navio foi completamente atingido
        if all(posicao['atingido'] for posicao in self.posicoes):  # Se todas as posições foram atingidas
            self.afundado = True  # Marca navio como afundado
        return self.afundado  # Retorna status


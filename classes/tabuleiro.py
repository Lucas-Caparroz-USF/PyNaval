class Tabuleiro:
    def __init__(self, tamanho=10):
        self.tamanho = tamanho  # Define tamanho do tabuleiro (10x10 por padrão)
        # Cria matriz do tabuleiro com dicionários para cada célula
        self.grid = [[{'navio': False, 'atingido': False} for _ in range(tamanho)] for _ in range(tamanho)]

    def exibir_tabuleiro(self):
        """
        Exibe o tabuleiro no console (para debug)
        'N' representa navio
        '~' representa água
        """
        for linha in self.grid:  # Para cada linha do tabuleiro
            linha_str = ""  # Inicializa string da linha
            for celula in linha:  # Para cada célula da linha
                if celula['navio']:  # Se há navio
                    linha_str += " N "  # Adiciona "N"
                else:  # Se não há navio
                    linha_str += " ~ "  # Adiciona "~"
            print(linha_str)  # Imprime linha no console
        print("\n")  # Pula uma linha após o tabuleiro

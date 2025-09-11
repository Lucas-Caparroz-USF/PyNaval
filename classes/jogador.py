from classes.tabuleiro import Tabuleiro
from classes.navio import Navio
import random

class Jogador:
    def __init__(self, nome):
        self.nome = nome                # Nome do jogador
        self.tabuleiro = Tabuleiro()    # Cria o tabuleiro do jogador
        self.navios = []                # Lista de navios do jogador

    def adicionar_navio(self, navio, posicoes):
        # Converte lista de tuplas em dicionários de posição
        navio.posicoes = [{'linha': l, 'coluna': c, 'atingido': False} for l, c in posicoes]
        for pos in navio.posicoes:  # Para cada posição do navio
            self.tabuleiro.grid[pos['linha']][pos['coluna']]['navio'] = navio  # Marca navio no tabuleiro
        self.navios.append(navio)  # Adiciona navio à lista

    def posicionar_navios_automatico(self):
        tipos_navios = [("Porta-aviões", 5), ("Encouraçado", 4),
                        ("Cruzador", 3), ("Submarino", 3), ("Destroyer", 2)]
        for nome, tamanho in tipos_navios:
            colocado = False  # Flag de posicionamento
            while not colocado:
                linha = random.randint(0, self.tabuleiro.tamanho - 1)  # Linha aleatória
                coluna = random.randint(0, self.tabuleiro.tamanho - 1)  # Coluna aleatória
                horizontal = random.choice([True, False])  # Orientação aleatória
                posicoes = []  # Lista de posições do navio
                try:
                    for i in range(tamanho):
                        if horizontal:
                            posicoes.append((linha, coluna + i))
                        else:
                            posicoes.append((linha + i, coluna))
                    if all(self.tabuleiro.grid[l][c]['navio'] is None for l, c in posicoes):
                        navio = Navio(tamanho, nome)  # Cria navio
                        self.adicionar_navio(navio, posicoes)  # Adiciona ao tabuleiro
                        colocado = True
                except IndexError:  # Se ultrapassar borda
                    continue

    def atacar(self, linha, coluna):  # Função de ataque
        """
        Realiza ataque na posição especificada.
        Retorna True se acertou navio, False caso contrário
        """
        celula = self.tabuleiro.grid[linha][coluna]  # Pega célula do tabuleiro
        if celula['atingido']:  # Se célula já foi atacada
            return None  # Nenhuma ação
        celula['atingido'] = True  # Marca célula como atacada
        if celula['navio']:  # Acertou navio
            celula['navio'].verificar_afundado()  # Verifica se navio afundou
            return True
        return False  # Errou

    def atacar_automatico(self, oponente):  # ✅ Novo método
        """
        Realiza ataque automático em posição aleatória do oponente
        """
        while True:  # Tenta até encontrar célula não atacada
            linha = random.randint(0, oponente.tabuleiro.tamanho - 1)  # Linha aleatória
            coluna = random.randint(0, oponente.tabuleiro.tamanho - 1)  # Coluna aleatória
            resultado = oponente.atacar(linha, coluna)  # Realiza ataque
            if resultado is not None:  # Se célula válida
                if resultado is True:  # Acerto
                    print(f"{self.nome} acertou navio do {oponente.nome} em ({linha}, {coluna})!")
                else:  # Erro
                    print(f"{self.nome} errou em ({linha}, {coluna}).")
                break  # Ataque concluído

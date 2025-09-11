from classes.jogador import Jogador  # Importa a classe Jogador

class Jogo:
    def __init__(self):
        self.jogador = Jogador("Jogador")  # Cria jogador
        self.inimigo = Jogador("Inimigo")  # Cria inimigo

    def iniciar(self):
        """
        Exibe mensagem de início de jogo no console
        """
        print("Jogo iniciado!")  # Mensagem de início
        print("Tabuleiro do jogador:")  # Mostra qual tabuleiro será exibido
        self.jogador.tabuleiro.exibir_tabuleiro()  # Exibe tabuleiro do jogador no console

    def verificar_vitoria(self):
        """
        Verifica se algum jogador venceu.
        Retorna:
            'Jogador' se jogador venceu
            'Inimigo' se inimigo venceu
            None se ainda não houve vitória
        """
        # Verifica se todos os navios do jogador foram afundados
        jogador_afundado = all(navio.afundado for navio in self.jogador.navios)
        # Verifica se todos os navios do inimigo foram afundados
        inimigo_afundado = all(navio.afundado for navio in self.inimigo.navios)

        if jogador_afundado:  # Todos navios do jogador foram afundados
            return "Inimigo"  # Inimigo venceu
        elif inimigo_afundado:  # Todos navios do inimigo foram afundados
            return "Jogador"  # Jogador venceu
        else:
            return None  # Ninguém venceu ainda

def desenhar_tabuleiro(tela, tabuleiro, pos_x, pos_y, celula=40):
    """
    Função para desenhar o tabuleiro na tela do Pygame
    """
    for i in range(tabuleiro.tamanho):  # Para cada linha
        for j in range(tabuleiro.tamanho):  # Para cada coluna
            rect = pygame.Rect(pos_x + j*celula, pos_y + i*celula, celula, celula)  # Retângulo da célula
            pygame.draw.rect(tela, (200,200,200), rect, 1)  # Desenha contorno da célula

# jogo.py
from .jogador import Jogador

class Jogo:
    def __init__(self):
        self.jogador = Jogador()
        self.inimigo = Jogador()

    def iniciar(self):
        """Posiciona navios automaticamente"""
        self.jogador.posicionar_navios_automatico()
        self.inimigo.posicionar_navios_automatico()

    def verificar_vitoria(self):
        """Verifica se todos navios do inimigo ou jogador foram afundados"""
        if all(navio.afundado() for navio in self.inimigo.navios):
            return "Jogador"
        if all(navio.afundado() for navio in self.jogador.navios):
            return "Inimigo"
        return None

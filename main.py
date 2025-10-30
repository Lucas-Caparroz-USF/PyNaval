import pygame
import random
from classes.jogo import Jogo
from classes.tabuleiro import desenhar_tabuleiro

pygame.init()

# ------------------- Configurações iniciais -------------------
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w - 25, info.current_h - 100
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PyNaval")

CELULA = 40
TAMANHO_TABULEIRO = 10
ESPACO = 100
MARGEM_SUPERIOR = 100
MARGEM_LATERAL = 60
ALTURA_CAIXA_MENSAGENS = 150

# Cores
AMARELO = (255, 255, 0)
AZUL = (0, 0, 64)
PRETO = (0,0,0)

# Fontes
fonte = pygame.font.SysFont(None, 48)
fonte_label = pygame.font.SysFont(None, 30)
letras = ["A","B","C","D","E","F","G","H","I","J"]

# Fundo
fundo = pygame.image.load("images/fundo.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
overlay = pygame.Surface((LARGURA, ALTURA))
overlay.set_alpha(100)
overlay.fill(PRETO)

# ------------------- Funções auxiliares -------------------

def desenhar_tela_inicio():
    TELA.blit(fundo, (0,0))
    TELA.blit(overlay, (0,0))
    titulo = fonte.render("PYNAVAL", True, AMARELO)
    TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, ALTURA//3))
    
    botoes = []
    niveis = ["Fácil", "Médio", "Difícil"]
    for i, nivel in enumerate(niveis):
        rect = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + i*70, 200, 50)
        pygame.draw.rect(TELA, AZUL, rect, border_radius=10)
        texto = fonte_label.render(nivel, True, AMARELO)
        TELA.blit(texto, (rect.centerx - texto.get_width()//2, rect.centery - texto.get_height()//2))
        botoes.append((rect, nivel))
    pygame.display.update()
    return botoes

def escolher_nivel():
    rodando_inicio = True
    nivel_selecionado = None
    botoes = desenhar_tela_inicio()
    while rodando_inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                for rect, nivel in botoes:
                    if rect.collidepoint(x, y):
                        nivel_selecionado = nivel
                        rodando_inicio = False
    return nivel_selecionado

def tela_vitoria(vencedor):
    rodando = True
    botoes = []
    while rodando:
        TELA.blit(fundo,(0,0))
        TELA.blit(overlay,(0,0))
        texto = fonte.render(f"{vencedor} venceu!", True, AMARELO)
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//3))
        
        # Botões
        rect_reiniciar = pygame.Rect(LARGURA//2 - 110, ALTURA//2, 220, 50)
        rect_fechar = pygame.Rect(LARGURA//2 - 110, ALTURA//2 + 70, 220, 50)
        pygame.draw.rect(TELA, AZUL, rect_reiniciar, border_radius=10)
        pygame.draw.rect(TELA, AZUL, rect_fechar, border_radius=10)
        texto_reiniciar = fonte_label.render("Reiniciar partida", True, AMARELO)
        TELA.blit(texto_reiniciar,
          (rect_reiniciar.centerx - texto_reiniciar.get_width()//2,
           rect_reiniciar.centery - texto_reiniciar.get_height()//2))
        texto_fechar = fonte_label.render("Fechar jogo", True, AMARELO)
        TELA.blit(texto_fechar,
          (rect_fechar.centerx - texto_fechar.get_width()//2,
           rect_fechar.centery - texto_fechar.get_height()//2))
        botoes = [(rect_reiniciar, "reiniciar"), (rect_fechar, "fechar")]
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                for rect, acao in botoes:
                    if rect.collidepoint(x, y):
                        return acao  # Retorna ação escolhida

def rodar_jogo(nivel):
    jogo = Jogo()
    jogo.iniciar()
    
    altura_total_retangulo = TAMANHO_TABULEIRO * CELULA + MARGEM_SUPERIOR + ALTURA_CAIXA_MENSAGENS
    retangulo_y = (ALTURA - altura_total_retangulo) // 2
    retangulo_x = (LARGURA - (2 * TAMANHO_TABULEIRO * CELULA + ESPACO + 2 * MARGEM_LATERAL)) // 2
    retangulo_largura = 2 * TAMANHO_TABULEIRO * CELULA + ESPACO + 2 * MARGEM_LATERAL
    retangulo_altura = altura_total_retangulo

    POS_X_JOGADOR = retangulo_x + MARGEM_LATERAL
    POS_Y_JOGADOR = retangulo_y + MARGEM_SUPERIOR
    POS_X_INIMIGO = POS_X_JOGADOR + TAMANHO_TABULEIRO * CELULA + ESPACO
    POS_Y_INIMIGO = POS_Y_JOGADOR

    turno_jogador = True
    mensagens = []
    MAX_MENSAGENS = 6
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "fechar"
            if evento.type == pygame.MOUSEBUTTONDOWN and turno_jogador:
                x, y = evento.pos
                linha = (y - POS_Y_INIMIGO) // CELULA
                coluna = (x - POS_X_INIMIGO) // CELULA
                if 0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO:
                    resultado = jogo.inimigo.tabuleiro.receber_tiro(linha, coluna)
                    if resultado in ["acertou","agua","afundou"]:
                        mensagens.append(f"{resultado} em ({linha},{coluna})" if resultado!="afundou" else "Afundou um navio!")
                        turno_jogador = False
                    elif resultado == "repetido":
                        mensagens.append("Selecione outra coordenada.")

        if not turno_jogador:
            while True:
                li, co = random.randint(0,9), random.randint(0,9)
                resultado = jogo.jogador.tabuleiro.receber_tiro(li, co)
                if resultado != "repetido":
                    mensagens.append(f"Inimigo atacou ({li},{co})")
                    break
            turno_jogador = True

        # Desenha tela
        TELA.blit(fundo,(0,0))
        TELA.blit(overlay,(0,0))
        pygame.draw.rect(TELA, AZUL, (retangulo_x, retangulo_y, retangulo_largura, retangulo_altura), border_radius=20)

        # Títulos
        titulo_jogador = fonte.render("JOGADOR", True, AMARELO)
        TELA.blit(titulo_jogador, (POS_X_JOGADOR + TAMANHO_TABULEIRO*CELULA//2 - titulo_jogador.get_width()//2, POS_Y_JOGADOR - MARGEM_SUPERIOR + 20))
        titulo_inimigo = fonte.render("ADVERSÁRIO", True, AMARELO)
        TELA.blit(titulo_inimigo, (POS_X_INIMIGO + TAMANHO_TABULEIRO*CELULA//2 - titulo_inimigo.get_width()//2, POS_Y_INIMIGO - MARGEM_SUPERIOR + 20))

        # Letras e números
        for i in range(TAMANHO_TABULEIRO):
            num_text = fonte_label.render(str(i), True, AMARELO)
            TELA.blit(num_text, (POS_X_JOGADOR + i*CELULA + CELULA//3, POS_Y_JOGADOR - CELULA//2))
            letra_text = fonte_label.render(letras[i], True, AMARELO)
            TELA.blit(letra_text, (POS_X_JOGADOR - CELULA//1.5, POS_Y_JOGADOR + i*CELULA + CELULA//4))

            TELA.blit(num_text, (POS_X_INIMIGO + i*CELULA + CELULA//3, POS_Y_INIMIGO - CELULA//2))
            TELA.blit(letra_text, (POS_X_INIMIGO - CELULA//1.5, POS_Y_INIMIGO + i*CELULA + CELULA//4))

        desenhar_tabuleiro(TELA, jogo.jogador.tabuleiro, POS_X_JOGADOR, POS_Y_JOGADOR, mostrar_navios=True)
        desenhar_tabuleiro(TELA, jogo.inimigo.tabuleiro, POS_X_INIMIGO, POS_Y_INIMIGO, mostrar_navios=False)

        y_mensagem = POS_Y_JOGADOR + TAMANHO_TABULEIRO * CELULA + 10
        for msg in mensagens[-MAX_MENSAGENS:]:
            texto_msg = fonte_label.render(msg, True, AMARELO)
            TELA.blit(texto_msg, (retangulo_x + 20, y_mensagem))
            y_mensagem += texto_msg.get_height() + 5

        vencedor = jogo.verificar_vitoria()
        if vencedor:
            acao = tela_vitoria(vencedor)
            if acao == "reiniciar":
                return rodar_jogo(nivel)  # Reinicia jogo
            else:
                pygame.quit()
                exit()

        pygame.display.update()

# ------------------- Programa principal -------------------
nivel = escolher_nivel()
rodar_jogo(nivel)
pygame.quit()

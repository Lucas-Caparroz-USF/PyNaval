# main.py
# Arquivo principal do PyNaval — versão compatível com a estrutura do projeto:
# pasta "classes" contendo jogo.py, tabuleiro.py, jogador.py, navio.py
# pasta "images" contendo fundo.jpg

import pygame
import random
from classes.jogo import Jogo                     # importa a classe Jogo do pacote classes
from classes.tabuleiro import desenhar_tabuleiro   # função que desenha um tabuleiro

# -------------------- Inicialização --------------------
pygame.init()

info = pygame.display.Info()
LARGURA, ALTURA = info.current_w - 25, info.current_h - 100
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PyNaval")

# -------------------- Configurações visuais --------------------
CELULA = 40
TAMANHO_TABULEIRO = 10
ESPACO = 100

MARGEM_SUPERIOR = 100
MARGEM_LATERAL = 60
ALTURA_CAIXA_MENSAGENS = 150

AMARELO = (255, 255, 0)
AZUL = (0, 0, 64)
PRETO = (0, 0, 0)

fonte = pygame.font.SysFont(None, 48)
fonte_label = pygame.font.SysFont(None, 30)
letras = ["A","B","C","D","E","F","G","H","I","J"]

# carrega imagem de fundo (ajuste caminho se necessário)
fundo = pygame.image.load("images/fundo.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

overlay = pygame.Surface((LARGURA, ALTURA))
overlay.set_alpha(100)
overlay.fill(PRETO)

# -------------------- Tela inicial (escolha de nível) --------------------
def desenhar_tela_inicio():
    """Desenha a tela inicial e retorna os retângulos dos botões."""
    TELA.blit(fundo, (0,0))
    TELA.blit(overlay, (0,0))
    titulo = fonte.render("PyNaval", True, AMARELO)
    TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, ALTURA//4))

    botoes = []
    niveis = ["Fácil", "Médio", "Difícil"]
    for i, nivel in enumerate(niveis):
        rect = pygame.Rect(LARGURA//2 - 120, ALTURA//2 + i*70, 240, 50)
        pygame.draw.rect(TELA, AZUL, rect, border_radius=10)
        texto = fonte_label.render(nivel, True, AMARELO)
        TELA.blit(texto, (rect.centerx - texto.get_width()//2, rect.centery - texto.get_height()//2))
        botoes.append((rect, nivel.lower()))
    pygame.display.update()
    return botoes

def escolher_nivel():
    """Mostra a tela inicial e espera o usuário escolher um nível."""
    botoes = desenhar_tela_inicio()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                for rect, nivel in botoes:
                    if rect.collidepoint(x, y):
                        return nivel  # "fácil", "médio" ou "difícil"

# -------------------- Tela de vitória com botões --------------------
def tela_vitoria(vencedor):
    """
    Exibe a tela de vitória com 2 botões:
    - Reiniciar partida -> retorna "reiniciar"
    - Fechar jogo -> retorna "fechar"
    """
    while True:
        TELA.blit(fundo, (0,0))
        TELA.blit(overlay, (0,0))
        texto = fonte.render(f"{vencedor} venceu!", True, AMARELO)
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//3))

        # botões (centralizados)
        largura_btn, altura_btn = 300, 50
        espaco_vertical = 20
        rect_reiniciar = pygame.Rect(LARGURA//2 - largura_btn//2, ALTURA//2, largura_btn, altura_btn)
        rect_fechar = pygame.Rect(LARGURA//2 - largura_btn//2, ALTURA//2 + altura_btn + espaco_vertical, largura_btn, altura_btn)

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

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_reiniciar.collidepoint(evento.pos):
                    return "reiniciar"
                if rect_fechar.collidepoint(evento.pos):
                    return "fechar"

# -------------------- IA do inimigo básica por nível --------------------
class InimigoAI:
    """
    IA simples configurável por nível.
    - facil: aleatório puro
    - medio: tenta adjacentes após acerto (memória simples)
    - dificil: varre o tabuleiro buscando não atingidas (simples heurística)
    """
    def __init__(self, nivel):
        self.nivel = nivel
        self.acertos_recentes = []  # (li,co) de acertos recentes

    def escolher_ataque(self, tabuleiro):
        tamanho = tabuleiro.tamanho

        # Fácil: aleatório até encontrar célula não atingida
        if self.nivel == "fácil":
            while True:
                li, co = random.randint(0,tamanho-1), random.randint(0,tamanho-1)
                if not tabuleiro.grid[li][co]['atingido']:
                    return li, co

        # Médio: se houver acertos recentes, tenta adjacentes; senão aleatório
        if self.nivel == "médio":
            for (ai, aj) in list(self.acertos_recentes):
                adj = [(ai-1,aj),(ai+1,aj),(ai,aj-1),(ai,aj+1)]
                random.shuffle(adj)
                for a,b in adj:
                    if 0<=a<tamanho and 0<=b<tamanho and not tabuleiro.grid[a][b]['atingido']:
                        return a,b
            # fallback aleatório
            while True:
                li, co = random.randint(0,tamanho-1), random.randint(0,tamanho-1)
                if not tabuleiro.grid[li][co]['atingido']:
                    return li, co

        # Difícil: varre priorizando centro (heurística simples), depois aleatório
        if self.nivel == "difícil":
            order = []
            # prioridade: centro-out spiral-like (simples)
            center = tamanho//2
            for d in range(tamanho):
                for i in range(tamanho):
                    for j in range(tamanho):
                        # heurística simples: priorizar células com distância menor ao centro
                        dist = abs(i-center) + abs(j-center)
                        order.append((dist, i, j))
            order.sort()
            for _, i, j in order:
                if not tabuleiro.grid[i][j]['atingido']:
                    return i, j
            # fallback aleatório (não deveria acontecer)
            while True:
                li, co = random.randint(0,tamanho-1), random.randint(0,tamanho-1)
                if not tabuleiro.grid[li][co]['atingido']:
                    return li, co

# -------------------- Função principal que roda o jogo --------------------
def rodar_jogo():
    nivel = escolher_nivel()  # "fácil", "médio" ou "difícil"
    ai = InimigoAI(nivel)

    # cria o jogo e posiciona os navios automaticamente
    jogo = Jogo()
    jogo.iniciar()

    mensagens = []
    MAX_MENSAGENS = 6
    turno_jogador = True

    # --- cálculo do retângulo azul centralizado e ampliado ---
    largura_total_tabuleiros = 2 * TAMANHO_TABULEIRO * CELULA + ESPACO
    altura_total_retangulo = TAMANHO_TABULEIRO * CELULA + MARGEM_SUPERIOR + ALTURA_CAIXA_MENSAGENS

    # margens extras para "aumentar" o retângulo sem deslocar tabuleiros
    margem_extra_x = 60  # pixels extras horizontais (metade de cada lado)
    margem_extra_y = 40  # pixels extras verticais (metade em cima e baixo)

    retangulo_largura = largura_total_tabuleiros + 2 * MARGEM_LATERAL + 2 * margem_extra_x
    retangulo_altura = altura_total_retangulo + 2 * margem_extra_y

    retangulo_x = (LARGURA - retangulo_largura) // 2
    retangulo_y = (ALTURA - retangulo_altura) // 2

    # tabuleiros posicionados dentro do retângulo, centralizados
    POS_X_JOGADOR = retangulo_x + MARGEM_LATERAL + margem_extra_x
    POS_Y_JOGADOR = retangulo_y + MARGEM_SUPERIOR + margem_extra_y
    POS_X_INIMIGO = POS_X_JOGADOR + TAMANHO_TABULEIRO * CELULA + ESPACO
    POS_Y_INIMIGO = POS_Y_JOGADOR

    # loop principal
    rodando = True
    clock = pygame.time.Clock()
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            # clique do jogador no tabuleiro inimigo
            if evento.type == pygame.MOUSEBUTTONDOWN and turno_jogador:
                x, y = evento.pos
                linha = (y - POS_Y_INIMIGO) // CELULA
                coluna = (x - POS_X_INIMIGO) // CELULA
                if 0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO:
                    resultado = jogo.inimigo.tabuleiro.receber_tiro(linha, coluna)
                    # Mensagens: usa "Errou" ao inves de "agua"
                    if resultado == "acertou":
                        mensagens.append(f"Acertou navio em ({letras[linha]},{coluna})!")
                        # registra acerto na IA caso vá usar adjacentes
                        ai.acertos_recentes.append((linha, coluna))
                        if len(ai.acertos_recentes) > 8:
                            ai.acertos_recentes.pop(0)
                        turno_jogador = False
                    elif resultado == "agua":
                        mensagens.append(f"Errou em ({letras[linha]},{coluna}).")
                        turno_jogador = False
                    elif resultado == "afundou":
                        mensagens.append("Afundou um navio!")
                        # limpa acertos recentes porque navio foi afundado
                        ai.acertos_recentes.clear()
                        turno_jogador = False
                    elif resultado == "repetido":
                        mensagens.append("Selecione outra coordenada.")

        # turno do inimigo (IA)
        if not turno_jogador:
            # escolhe posição pelo nível
            li, co = ai.escolher_ataque(jogo.jogador.tabuleiro)
            resultado_inimigo = jogo.jogador.tabuleiro.receber_tiro(li, co)
            if resultado_inimigo == "acertou":
                mensagens.append(f"Inimigo acertou em ({letras[li]},{co})")
                # registra para IA média/dificil
                ai.acertos_recentes.append((li,co))
                if len(ai.acertos_recentes) > 8:
                    ai.acertos_recentes.pop(0)
            elif resultado_inimigo == "agua":
                mensagens.append(f"Inimigo errou em ({letras[li]},{co})")
            elif resultado_inimigo == "afundou":
                mensagens.append("Inimigo afundou um navio!")
                ai.acertos_recentes.clear()
            turno_jogador = True

        # -------------------- Desenho --------------------
        TELA.blit(fundo, (0,0))
        TELA.blit(overlay, (0,0))

        # retângulo azul atrás dos tabuleiros
        pygame.draw.rect(TELA, AZUL, (retangulo_x, retangulo_y, retangulo_largura, retangulo_altura), border_radius=20)

        # títulos
        titulo_j = fonte.render("JOGADOR", True, AMARELO)
        TELA.blit(titulo_j, (POS_X_JOGADOR + (TAMANHO_TABULEIRO*CELULA)//2 - titulo_j.get_width()//2,
                             POS_Y_JOGADOR - MARGEM_SUPERIOR + 20))
        titulo_i = fonte.render("ADVERSÁRIO", True, AMARELO)
        TELA.blit(titulo_i, (POS_X_INIMIGO + (TAMANHO_TABULEIRO*CELULA)//2 - titulo_i.get_width()//2,
                             POS_Y_INIMIGO - MARGEM_SUPERIOR + 20))

        # letras e números
        for i in range(TAMANHO_TABULEIRO):
            num_text = fonte_label.render(str(i), True, AMARELO)
            letra_text = fonte_label.render(letras[i], True, AMARELO)
            # jogador (topo números / esquerda letras)
            TELA.blit(num_text, (POS_X_JOGADOR + i*CELULA + CELULA//3, POS_Y_JOGADOR - CELULA//2))
            TELA.blit(letra_text, (POS_X_JOGADOR - CELULA//1.5, POS_Y_JOGADOR + i*CELULA + CELULA//4))
            # inimigo
            TELA.blit(num_text, (POS_X_INIMIGO + i*CELULA + CELULA//3, POS_Y_INIMIGO - CELULA//2))
            TELA.blit(letra_text, (POS_X_INIMIGO - CELULA//1.5, POS_Y_INIMIGO + i*CELULA + CELULA//4))

        # desenha os tabuleiros (mostrar navios do jogador)
        desenhar_tabuleiro(TELA, jogo.jogador.tabuleiro, POS_X_JOGADOR, POS_Y_JOGADOR, mostrar_navios=True)
        desenhar_tabuleiro(TELA, jogo.inimigo.tabuleiro, POS_X_INIMIGO, POS_Y_INIMIGO, mostrar_navios=False)

        # mensagens inferior
        y_mensagem = POS_Y_JOGADOR + TAMANHO_TABULEIRO * CELULA + 10
        for msg in mensagens[-MAX_MENSAGENS:]:
            texto_msg = fonte_label.render(msg, True, AMARELO)
            TELA.blit(texto_msg, (retangulo_x + 20, y_mensagem))
            y_mensagem += texto_msg.get_height() + 5

        # verifica vitória
        vencedor = jogo.verificar_vitoria()
        if vencedor:
            acao = tela_vitoria(vencedor)
            if acao == "reiniciar":
                # reinicia o jogo (simplesmente chama novamente a função principal)
                return rodar_jogo()
            else:
                pygame.quit()
                exit()

        pygame.display.update()
        pygame.time.Clock().tick(30)

# -------------------- Inicia o programa --------------------
if __name__ == "__main__":
    rodar_jogo()

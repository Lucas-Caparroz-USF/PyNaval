import pygame  # Importa a biblioteca Pygame
from classes.jogo import Jogo, desenhar_tabuleiro  # Importa classe Jogo e função para desenhar tabuleiros

pygame.init()  # Inicializa todos os módulos do Pygame

# Configuração da janela do jogo
LARGURA, ALTURA = 950, 600  # Largura e altura da janela
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela
pygame.display.set_caption("PyNaval")  # Define o título da janela

CELULA = 40  # Define o tamanho de cada célula do tabuleiro em pixels

# Cria o objeto do jogo
jogo = Jogo()  # Instancia a classe Jogo
jogo.jogador.posicionar_navios_automatico()  # Posiciona navios do jogador automaticamente
jogo.inimigo.posicionar_navios_automatico()  # Posiciona navios do inimigo automaticamente
jogo.iniciar()  # Exibe tabuleiro do jogador no console (para debug)

# Define posições iniciais dos tabuleiros na tela
POS_X_JOGADOR = 50  # Coordenada X do tabuleiro do jogador
POS_Y_JOGADOR = 50  # Coordenada Y do tabuleiro do jogador
POS_X_INIMIGO = 500  # Coordenada X do tabuleiro do inimigo
POS_Y_INIMIGO = 50   # Coordenada Y do tabuleiro do inimigo

turno_jogador = True  # Define que o jogador começa jogando

# Cria fonte para exibir mensagens de vitória
fonte = pygame.font.SysFont(None, 48)  # Fonte padrão, tamanho 48

rodando = True  # Flag para controlar o loop principal do jogo

# Loop principal do jogo
while rodando:
    # Captura eventos do Pygame
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Se o jogador fechar a janela
            rodando = False  # Encerra o loop do jogo

        # Verifica clique do jogador no tabuleiro inimigo
        if evento.type == pygame.MOUSEBUTTONDOWN and turno_jogador:  # Só se for o turno do jogador
            x, y = evento.pos  # Pega posição do clique
            linha = (y - POS_Y_INIMIGO) // CELULA  # Calcula linha clicada no tabuleiro inimigo
            coluna = (x - POS_X_INIMIGO) // CELULA  # Calcula coluna clicada no tabuleiro inimigo
            # Verifica se o clique está dentro dos limites do tabuleiro
            if 0 <= linha < jogo.inimigo.tabuleiro.tamanho and 0 <= coluna < jogo.inimigo.tabuleiro.tamanho:
                resultado = jogo.inimigo.atacar(linha, coluna)  # Realiza ataque
                if resultado is True:  # Acertou navio
                    print(f"Jogador acertou o navio na posição ({linha}, {coluna})!")
                elif resultado is False:  # Errou
                    print(f"Jogador errou na posição ({linha}, {coluna}).")
                turno_jogador = False  # Passa o turno para o inimigo

    # Turno automático do inimigo
    if not turno_jogador:  # Só se for turno do inimigo
        jogo.inimigo.atacar_automatico(jogo.jogador)  # Inimigo realiza ataque automático
        turno_jogador = True  # Retorna o turno para o jogador

    # Preenche a tela com azul (representa água)
    TELA.fill((0, 102, 204))

    # Desenha tabuleiro do jogador
    desenhar_tabuleiro(TELA, jogo.jogador.tabuleiro, POS_X_JOGADOR, POS_Y_JOGADOR)
    # Desenha tabuleiro do inimigo
    desenhar_tabuleiro(TELA, jogo.inimigo.tabuleiro, POS_X_INIMIGO, POS_Y_INIMIGO)

    # Destaca células atacadas do inimigo
    for i in range(jogo.inimigo.tabuleiro.tamanho):  # Percorre linhas
        for j in range(jogo.inimigo.tabuleiro.tamanho):  # Percorre colunas
            celula = jogo.inimigo.tabuleiro.grid[i][j]  # Pega célula
            if celula['atingido']:  # Se a célula foi atacada
                cor = (255, 0, 0) if celula['navio'] else (255, 255, 255)  # Vermelho se navio, branco se água
                ret = pygame.Rect(POS_X_INIMIGO + j*CELULA, POS_Y_INIMIGO + i*CELULA, CELULA, CELULA)  # Retângulo da célula
                pygame.draw.rect(TELA, cor, ret)  # Desenha célula
                pygame.draw.rect(TELA, (0,0,0), ret, 1)  # Desenha contorno preto

    # Destaca células atacadas do jogador
    for i in range(jogo.jogador.tabuleiro.tamanho):  # Percorre linhas
        for j in range(jogo.jogador.tabuleiro.tamanho):  # Percorre colunas
            celula = jogo.jogador.tabuleiro.grid[i][j]  # Pega célula
            if celula['atingido']:  # Se foi atacada
                cor = (255, 0, 0) if celula['navio'] else (255, 255, 255)  # Vermelho se navio, branco se água
                ret = pygame.Rect(POS_X_JOGADOR + j*CELULA, POS_Y_JOGADOR + i*CELULA, CELULA, CELULA)  # Retângulo da célula
                pygame.draw.rect(TELA, cor, ret)  # Desenha célula
                pygame.draw.rect(TELA, (0,0,0), ret, 1)  # Desenha contorno preto

    # Verifica se alguém venceu
    vencedor = jogo.verificar_vitoria()  # Chama função de vitória
    if vencedor:  # Se houver vencedor
        texto = fonte.render(f"{vencedor} venceu!", True, (255,255,0))  # Cria texto em amarelo
        # Centraliza mensagem na tela
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - texto.get_height()//2))
        pygame.display.update()  # Atualiza tela para mostrar mensagem
        pygame.time.delay(5000)  # Aguarda 5 segundos
        break  # Sai do loop principal

    pygame.display.update()  # Atualiza a tela do Pygame a cada frame

pygame.quit()  # Encerra o Pygame ao sair do loop

import pygame  # Biblioteca gráfica
import random  # Para ataques automáticos do inimigo
from classes.jogo import Jogo  # Classe principal do jogo
from classes.tabuleiro import desenhar_tabuleiro  # Função para desenhar tabuleiros

pygame.init()  # Inicializa todos os módulos do pygame

# Captura resolução do monitor
info = pygame.display.Info()  # Obtém informações do monitor
LARGURA, ALTURA = info.current_w - 25, info.current_h - 100  # Define tamanho da janela

# Cria janela
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Janela do jogo
pygame.display.set_caption("PyNaval")  # Título da janela

# Tamanho das células e tabuleiros
CELULA = 40  # Pixels por célula
TAMANHO_TABULEIRO = 10  # 10x10 células

# Carrega imagem de fundo
fundo = pygame.image.load("images/fundo.jpg")  # Caminho da imagem
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Redimensiona para tela

# Overlay semitransparente para escurecer fundo
overlay = pygame.Surface((LARGURA, ALTURA))  # Superfície da tela
overlay.set_alpha(100)  # Transparência (0-255)
overlay.fill((0, 0, 0))  # Preenche com preto

# Cria objeto do jogo
jogo = Jogo()  # Instancia classe Jogo
jogo.iniciar()  # Posiciona navios automaticamente
print("Navios posicionados para Jogador e Inimigo.")  # Debug

# Espaço entre tabuleiros
ESPACO = 100

# Centraliza os tabuleiros
POS_X_JOGADOR = (LARGURA - (TAMANHO_TABULEIRO * CELULA * 2 + ESPACO)) // 2
POS_Y_JOGADOR = (ALTURA - (TAMANHO_TABULEIRO * CELULA)) // 2
POS_X_INIMIGO = POS_X_JOGADOR + TAMANHO_TABULEIRO * CELULA + ESPACO
POS_Y_INIMIGO = POS_Y_JOGADOR

# Turno inicial do jogador
turno_jogador = True

# Fonte para mensagens de vitória
fonte = pygame.font.SysFont(None, 48)  # Fonte padrão tamanho 48

# Fonte para números, letras e mensagens
fonte_label = pygame.font.SysFont(None, 30)  # Fonte pequena amarela

# Letras para linhas
letras = ["A","B","C","D","E","F","G","H","I","J"]

# Margens do retângulo azul sólido
MARGEM_SUPERIOR = 100  # Mais espaço para títulos
MARGEM_LATERAL = 60  # Margem lateral
ALTURA_CAIXA_MENSAGENS = 150  # Altura da caixa de mensagens inferior

# Calcula limites do retângulo azul arredondado
retangulo_x = POS_X_JOGADOR - MARGEM_LATERAL
retangulo_y = POS_Y_JOGADOR - MARGEM_SUPERIOR
retangulo_largura = 2 * TAMANHO_TABULEIRO * CELULA + ESPACO + 2 * MARGEM_LATERAL
retangulo_altura = TAMANHO_TABULEIRO * CELULA + MARGEM_SUPERIOR + ALTURA_CAIXA_MENSAGENS

# Lista para armazenar mensagens exibidas na tela
mensagens = []  # Cada elemento será uma string
MAX_MENSAGENS = 6  # Número máximo de mensagens visíveis

rodando = True  # Controla loop principal

# Loop principal do jogo
while rodando:
    try:
        # Captura eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Fechar janela
                rodando = False

            # Clique do jogador no tabuleiro inimigo
            if evento.type == pygame.MOUSEBUTTONDOWN and turno_jogador:
                x, y = evento.pos  # Pega posição do clique
                linha = (y - POS_Y_INIMIGO) // CELULA  # Calcula linha
                coluna = (x - POS_X_INIMIGO) // CELULA  # Calcula coluna

                # Verifica se clique está dentro do tabuleiro
                if 0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO:
                    resultado = jogo.inimigo.tabuleiro.receber_tiro(linha, coluna)
                    if resultado == "acertou":
                        msg = f"Acertou navio em ({linha},{coluna})!"
                        print(msg)
                        mensagens.append(msg)
                        turno_jogador = False
                    elif resultado == "agua":
                        msg = f"Errou em ({linha},{coluna})."
                        print(msg)
                        mensagens.append(msg)
                        turno_jogador = False
                    elif resultado == "afundou":
                        msg = f"Afundou um navio!"
                        print(msg)
                        mensagens.append(msg)
                        turno_jogador = False
                    elif resultado == "repetido":
                        msg = "Selecione outra coordenada."
                        print(msg)
                        mensagens.append(msg)

        # Turno do inimigo
        if not turno_jogador:
            while True:
                li, co = random.randint(0, 9), random.randint(0, 9)
                resultado = jogo.jogador.tabuleiro.receber_tiro(li, co)
                if resultado != "repetido":
                    msg = f"Inimigo atacou ({li},{co})"
                    print(msg)
                    mensagens.append(msg)
                    break
            turno_jogador = True

        # Desenha fundo
        TELA.blit(fundo, (0, 0))  # Fundo
        TELA.blit(overlay, (0, 0))  # Escurece fundo

        # Desenha retângulo azul sólido arredondado envolvendo os tabuleiros e área de mensagens
        pygame.draw.rect(TELA, (0, 0, 64),
                         (retangulo_x, retangulo_y, retangulo_largura, retangulo_altura),
                         border_radius=20)

        # Títulos acima dos tabuleiros
        titulo_jogador = fonte.render("JOGADOR", True, (255, 255, 0))
        TELA.blit(titulo_jogador,
                  (POS_X_JOGADOR + TAMANHO_TABULEIRO*CELULA//2 - titulo_jogador.get_width()//2,
                   POS_Y_JOGADOR - MARGEM_SUPERIOR + 20))

        titulo_inimigo = fonte.render("ADVERSÁRIO", True, (255, 255, 0))
        TELA.blit(titulo_inimigo,
                  (POS_X_INIMIGO + TAMANHO_TABULEIRO*CELULA//2 - titulo_inimigo.get_width()//2,
                   POS_Y_INIMIGO - MARGEM_SUPERIOR + 20))

        # Letras e números tabuleiro jogador
        for i in range(TAMANHO_TABULEIRO):
            num_text = fonte_label.render(str(i), True, (255, 255, 0))
            TELA.blit(num_text, (POS_X_JOGADOR + i*CELULA + CELULA//3, POS_Y_JOGADOR - CELULA//2))
            letra_text = fonte_label.render(letras[i], True, (255, 255, 0))
            TELA.blit(letra_text, (POS_X_JOGADOR - CELULA//1.5, POS_Y_JOGADOR + i*CELULA + CELULA//4))

        # Letras e números tabuleiro inimigo
        for i in range(TAMANHO_TABULEIRO):
            num_text = fonte_label.render(str(i), True, (255, 255, 0))
            TELA.blit(num_text, (POS_X_INIMIGO + i*CELULA + CELULA//3, POS_Y_INIMIGO - CELULA//2))
            letra_text = fonte_label.render(letras[i], True, (255, 255, 0))
            TELA.blit(letra_text, (POS_X_INIMIGO - CELULA//1.5, POS_Y_INIMIGO + i*CELULA + CELULA//4))

        # Desenha tabuleiros
        desenhar_tabuleiro(TELA, jogo.jogador.tabuleiro, POS_X_JOGADOR, POS_Y_JOGADOR, mostrar_navios=True)
        desenhar_tabuleiro(TELA, jogo.inimigo.tabuleiro, POS_X_INIMIGO, POS_Y_INIMIGO, mostrar_navios=False)

        # Exibe mensagens na parte inferior do retângulo
        y_mensagem = POS_Y_JOGADOR + TAMANHO_TABULEIRO * CELULA + 10
        for msg in mensagens[-MAX_MENSAGENS:]:  # Últimas mensagens
            texto_msg = fonte_label.render(msg, True, (255, 255, 0))
            TELA.blit(texto_msg, (retangulo_x + 20, y_mensagem))
            y_mensagem += texto_msg.get_height() + 5

        # Verifica vitória
        vencedor = jogo.verificar_vitoria()
        if vencedor:
            texto = fonte.render(f"{vencedor} venceu!", True, (255, 255, 0))
            TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - texto.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        # Atualiza tela
        pygame.display.update()

    except Exception as e:
        print("Erro:", e)
        mensagens.append(f"Erro: {e}")
        rodando = False

pygame.quit()  # Encerra pygame

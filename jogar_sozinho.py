import os
import pickle
import random
import neat
import pygame

pygame.init()

LARGURA = 800
ALTURA = 400
CHAO_Y = 320
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dino Campeao - Modelo Pickle")
FONTE = pygame.font.SysFont("arial", 20)


class Dinossauro:
    def __init__(self):
        self.x = 60
        self.largura = 30
        self.altura_normal = 50
        self.altura_abaixado = 25
        self.altura = self.altura_normal
        self.y = CHAO_Y - self.altura
        self.vel_y = 0
        self.pulando = False
        self.abaixado = False
        self.cor = (30, 160, 80)  # Verde destaque para o campeao

    def pular(self):
        if not self.pulando and not self.abaixado:
            self.vel_y = -15
            self.pulando = True

    def abaixar(self, estado):
        if not self.pulando:
            self.abaixado = estado
            if estado:
                self.altura = self.altura_abaixado
                self.y = CHAO_Y - self.altura
            else:
                self.altura = self.altura_normal
                self.y = CHAO_Y - self.altura

    def atualizar(self):
        if self.pulando:
            self.y += self.vel_y
            self.vel_y += 0.95
            if self.y >= CHAO_Y - self.altura:
                self.y = CHAO_Y - self.altura
                self.pulando = False
                self.vel_y = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.get_rect())


class Obstaculo:
    def __init__(self, velocidade):
        self.x = LARGURA + random.randint(0, 60)
        self.velocidade = velocidade
        tipo = random.random()

        if tipo < 0.45:
            self.largura = random.choice()
            self.altura = random.choice()
            self.y = CHAO_Y - self.altura
            self.cor = (200, 50, 50)
        elif tipo < 0.70:
            self.largura = 70
            self.altura = 40
            self.y = CHAO_Y - self.altura
            self.cor = (160, 20, 20)
        else:
            self.largura = 45
            self.altura = 25
            self.y = random.choice([CHAO_Y - 28, CHAO_Y - 45, CHAO_Y - 75])
            self.cor = (50, 80, 200)

    def atualizar(self):
        self.x -= self.velocidade

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.get_rect())


def jogar_com_campeao(config_path, modelo_path):
    if not os.path.exists(modelo_path):
        print(f"Erro: Arquivo '{modelo_path}' nao encontrado! Rode o dino_ia.py ate o fim primeiro.")
        return

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Carrega o genoma vencedor salvo com pickle
    with open(modelo_path, "rb") as f:
        genoma_campeao = pickle.load(f)

    # Reconstroi a rede neural a partir do genoma salvo
    rede_neural = neat.nn.FeedForwardNetwork.create(genoma_campeao, config)

    dino = Dinossauro()
    velocidade_jogo = 9
    obstaculos = [Obstaculo(velocidade_jogo)]
    pontos = 0
    recorde = 0
    clock = pygame.time.Clock()

    rodando = True
    while rodando:
        clock.tick(60)  # Velocidade normal de jogo (60 FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        pontos += 1
        if pontos > recorde:
            recorde = pontos

        if pontos % 120 == 0 and velocidade_jogo < 22:
            velocidade_jogo += 0.6

        distancia_spawn = max(210, int(380 - velocidade_jogo * 5))
        if len(obstaculos) == 0 or obstaculos[-1].x < LARGURA - random.randint(distancia_spawn, distancia_spawn + 180):
            obstaculos.append(Obstaculo(velocidade_jogo))

        for obs in list(obstaculos):
            obs.velocidade = velocidade_jogo
            obs.atualizar()
            if obs.x + obs.largura < 0:
                obstaculos.remove(obs)

        proximo_obs = None
        for obs in obstaculos:
            if obs.x + obs.largura > 60:
                proximo_obs = obs
                break

        dino.atualizar()

        if proximo_obs:
            distancia = proximo_obs.x - dino.x
            inputs = (distancia, proximo_obs.y, proximo_obs.largura, velocidade_jogo)
        else:
            inputs = (LARGURA, CHAO_Y, 0, velocidade_jogo)

        output = rede_neural.activate(inputs)

        if output > 0.5:
            dino.abaixar(False)
            dino.pular()
        elif output > 0.5:
            dino.abaixar(True)
        else:
            dino.abaixar(False)

        # Se bater, reinicia a partida automaticamente para continuar assistindo
        if proximo_obs and dino.get_rect().colliderect(proximo_obs.get_rect()):
            dino = Dinossauro()
            velocidade_jogo = 9
            obstaculos = [Obstaculo(velocidade_jogo)]
            pontos = 0

        TELA.fill((245, 245, 245))
        pygame.draw.line(TELA, (100, 100, 100), (0, CHAO_Y), (LARGURA, CHAO_Y), 2)

        for obs in obstaculos:
            obs.desenhar()

        dino.desenhar()

        texto_status = FONTE.render("MODO EXIBICAO (Campeao Pickle)", True, (30, 130, 60))
        texto_pontos = FONTE.render(f"Pontos: {pontos} | Recorde: {recorde}", True, (0, 0, 0))
        texto_vel = FONTE.render(f"Velocidade: {velocidade_jogo:.1f}", True, (0, 0, 0))

        TELA.blit(texto_status, (10, 10))
        TELA.blit(texto_pontos, (10, 35))
        TELA.blit(texto_vel, (10, 60))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    local_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    modelo_path = os.path.join(local_dir, "melhor_dino.pkl")
    jogar_com_campeao(config_path, modelo_path)

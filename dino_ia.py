from sprites import DINO_EM_PE_1, DINO_EM_PE_2, DINO_AGACHADO_1, DINO_AGACHADO_2, criar_sprite_dino
from sprites import DINO_EM_PE_1, DINO_EM_PE_2, DINO_AGACHADO_1, DINO_AGACHADO_2, criar_sprite_dino
import os
import glob
import pickle
import random
import neat
import pygame

pygame.init()

LARGURA = 800
ALTURA = 400
CHAO_Y = 320
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dino IA - Zona Movel (5 Locais)")
FONTE = pygame.font.SysFont("arial", 20)

geracao = 0
LOCAIS_ZONA = (65, 130, 195, 260, 325)
LARGURA_ZONA = 70


class Dinossauro:
    def __init__(self):
        self.x, self.min_x, self.max_x, self.vel_x = 185, 20, 350, 5
        self.largura_normal, self.largura_abaixado = 30, 45
        self.altura_normal, self.altura_abaixado = 50, 24
        self.largura, self.altura = self.largura_normal, self.altura_normal
        self.y = CHAO_Y - self.altura
        self.vel_y, self.pulando, self.abaixado = 0, False, False
        self.cor = (random.randint(40, 210), random.randint(40, 210), random.randint(40, 210))
        self.sprites_pe = [criar_sprite_dino(DINO_EM_PE_1, self.cor, 2), criar_sprite_dino(DINO_EM_PE_2, self.cor, 2)]
        self.sprites_agachado = [criar_sprite_dino(DINO_AGACHADO_1, self.cor, 2), criar_sprite_dino(DINO_AGACHADO_2, self.cor, 2)]

    def mover_esquerda(self):
        self.x = max(self.min_x, self.x - self.vel_x)

    def mover_direita(self):
        self.x = min(self.max_x, self.x + self.vel_x)

    def pular(self):
        if not self.pulando and not self.abaixado:
            self.vel_y = -15
            self.pulando = True

    def abaixar(self, estado):
        if estado:
            if self.pulando:
                if self.vel_y < 14:
                    self.vel_y = 14
            else:
                self.abaixado = True
                self.altura = self.altura_abaixado
                self.largura = self.largura_abaixado
                self.y = CHAO_Y - self.altura
        else:
            if not self.pulando and self.abaixado:
                self.abaixado = False
                self.altura = self.altura_normal
                self.largura = self.largura_normal
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
        frame = (pygame.time.get_ticks() // 90) % 2
        if self.abaixado:
            TELA.blit(self.sprites_agachado[frame], (int(self.x) - 8, int(self.y) - 22))
        else:
            TELA.blit(self.sprites_pe[frame], (int(self.x) - 7, int(self.y) + 2))

class Obstaculo:
    def __init__(self, velocidade):
        self.x = LARGURA + random.randint(0, 80)
        self.velocidade = velocidade
        tipo = random.random()

        if tipo < 0.45:
            self.largura = random.choice((20, 30, 45))
            self.altura = random.choice((35, 50))
            self.y = CHAO_Y - self.altura
            self.cor = (200, 50, 50)
        elif tipo < 0.70:
            self.largura = 65
            self.altura = 40
            self.y = CHAO_Y - self.altura
            self.cor = (160, 20, 20)
        else:
            self.largura = 45
            self.altura = 24
            self.y = random.choice((CHAO_Y - 26, CHAO_Y - 46, CHAO_Y - 62, CHAO_Y - 85))
            self.cor = (50, 80, 200)

    def atualizar(self):
        self.x -= self.velocidade

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self):
        pygame.draw.rect(TELA, self.cor, self.get_rect())


def eval_genomes(genomes, config):
    global geracao
    geracao += 1

    nets = []
    ge = []
    dinos = []

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Dinossauro())
        ge.append(genome)

    velocidade_jogo = 5.0
    direcao_vel = 1

    indice_zona = 2
    centro_zona = LOCAIS_ZONA[indice_zona]

    obstaculos = [Obstaculo(velocidade_jogo)]
    pontos = 0
    clock = pygame.time.Clock()

    rodando = True
    while rodando and len(dinos) > 0:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if ge:
                    melhor_atual = max(ge, key=lambda g: g.fitness)
                    with open("melhor_dino.pkl", "wb") as f:
                        pickle.dump(melhor_atual, f)
                    print("\nJanela fechada! Melhor dinossauro salvo em 'melhor_dino.pkl'.")
                pygame.quit()
                quit()

        pontos += 1

        if pontos % 80 == 0:
            velocidade_jogo += 0.5 * direcao_vel
            if velocidade_jogo >= 10.0:
                velocidade_jogo = 10.0
                direcao_vel = -1
            elif velocidade_jogo <= 5.0:
                velocidade_jogo = 5.0
                direcao_vel = 1

        if pontos % 90 == 0:
            novas_opcoes = [idx for idx in range(5) if idx != indice_zona]
            indice_zona = random.choice(novas_opcoes)
            centro_zona = LOCAIS_ZONA[indice_zona]

        # Espacamento fiel ao Chrome Dino original: folga proporcional a velocidade + intervalo amplo
        gap_minimo = int(velocidade_jogo * 42 + 240)
        gap_maximo = gap_minimo + 260
        if len(obstaculos) == 0 or obstaculos[-1].x < LARGURA - random.randint(gap_minimo, gap_maximo):
            obstaculos.append(Obstaculo(velocidade_jogo))

        for obs in list(obstaculos):
            obs.velocidade = velocidade_jogo
            obs.atualizar()
            if obs.x + obs.largura < 0:
                obstaculos.remove(obs)

        for i in range(len(dinos) - 1, -1, -1):
            dino = dinos[i]
            dino.atualizar()

            # Progressao continua cobrindo todo o mapa: 1.0 ponto no centro da zona ate 0.1 no extremo mais longe
            centro_dino = dino.x + (dino.largura / 2.0)
            dist_zona = abs(centro_dino - centro_zona)
            dist_maxima = 360.0
            fator = max(0.0, min(1.0, 1.0 - (dist_zona / dist_maxima)))
            pontos_zona = 0.1 + (0.9 * fator)
            ge[i].fitness += pontos_zona

            proximo_obs = None
            for obs in obstaculos:
                if obs.x + obs.largura > dino.x:
                    proximo_obs = obs
                    break

            # Direcao relativa: negativo = zona esta a esquerda | positivo = zona esta a direita | 0 = em cima
            delta_zona = (centro_zona - centro_dino) / 300.0
            dist_abs_norm = abs(centro_zona - centro_dino) / 300.0

            if proximo_obs:
                dist_px = max(0.0, proximo_obs.x - dino.x)
                proximidade = max(0.0, 1.0 - (dist_px / 450.0))
                obs_y = (CHAO_Y - proximo_obs.y) / 100.0
                obs_larg = proximo_obs.largura / 100.0
                vel_norm = velocidade_jogo / 10.0
                inputs = (proximidade, obs_y, obs_larg, vel_norm, delta_zona, dist_abs_norm)
            else:
                inputs = (0.0, 0.0, 0.0, velocidade_jogo / 10.0, delta_zona, dist_abs_norm)

            val_pular, val_abaixar, val_esq, val_dir = nets[i].activate(inputs)

            if val_esq > 0.5 and val_dir <= 0.5:
                dino.mover_esquerda()
            elif val_dir > 0.5 and val_esq <= 0.5:
                dino.mover_direita()

            if val_pular > 0.5 and not dino.pulando:
                dino.abaixar(False)
                dino.pular()
                if not proximo_obs or (proximo_obs.x - dino.x) > 260:
                    ge[i].fitness -= 2.5
            elif val_abaixar > 0.5:
                dino.abaixar(True)
                if proximo_obs and proximo_obs.y in (CHAO_Y - 46, CHAO_Y - 62) and not dino.pulando:
                    ge[i].fitness += 0.05
            else:
                dino.abaixar(False)

            if proximo_obs and dino.get_rect().colliderect(proximo_obs.get_rect()):
                ge[i].fitness -= 1
                dinos.pop(i)
                nets.pop(i)
                ge.pop(i)

        TELA.fill((245, 245, 245))
        # Desenha o gradiente continuo de pontos no chao (0.1 nas pontas -> 1.0 no centro da zona)
        for px in range(20, 395, 3):
            f = max(0.0, min(1.0, 1.0 - (abs(px - centro_zona) / 360.0)))
            r = int(255 - (175 * f))
            g = int(235 - (25 * f))
            b = int(170 - (70 * f))
            pygame.draw.rect(TELA, (r, g, b), (px, CHAO_Y, 3, 10))
        pygame.draw.line(TELA, (20, 140, 40), (centro_zona, CHAO_Y - 6), (centro_zona, CHAO_Y + 12), 3)

        for pos in LOCAIS_ZONA:
            pygame.draw.line(TELA, (120, 120, 120), (pos, CHAO_Y + 10), (pos, CHAO_Y + 15), 2)

        pygame.draw.line(TELA, (100, 100, 100), (0, CHAO_Y), (LARGURA, CHAO_Y), 2)
        pygame.draw.line(TELA, (210, 210, 210), (395, 50), (395, CHAO_Y), 1)

        for obs in obstaculos:
            obs.desenhar()

        for dino in dinos:
            dino.desenhar()

        seta = "↑" if direcao_vel == 1 else "↓"
        texto_geracao = FONTE.render(f"Geracao: {geracao}", True, (0, 0, 0))
        texto_vivos = FONTE.render(f"Vivos: {len(dinos)}", True, (0, 0, 0))
        texto_pontos = FONTE.render(f"Pontos: {pontos} | Vel: {velocidade_jogo:.1f} {seta} | Zona: {indice_zona + 1}/5", True, (0, 0, 0))

        TELA.blit(texto_geracao, (10, 10))
        TELA.blit(texto_vivos, (10, 35))
        TELA.blit(texto_pontos, (10, 60))

        pygame.display.flip()


def run(config_path):
    global geracao
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    checkpoints = glob.glob("neat-checkpoint-*")
    if checkpoints:
        ultimo_checkpoint = max(checkpoints, key=lambda x: int(x.split("-")[-1]))
        print(f"Carregando progresso salvo de: {ultimo_checkpoint}")
        populacao = neat.Checkpointer.restore_checkpoint(ultimo_checkpoint)
        geracao = populacao.generation
    else:
        print("Iniciando novo treinamento do zero...")
        populacao = neat.Population(config)

    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.Checkpointer(generation_interval=5, filename_prefix="neat-checkpoint-"))

    vencedor = populacao.run(eval_genomes, 500)
    with open("melhor_dino.pkl", "wb") as f:
        pickle.dump(vencedor, f)
    print("Melhor dinossauro salvo em 'melhor_dino.pkl'!")


if __name__ == "__main__":
    local_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

class Obstaculo:
    def __init__(self, velocidade):
        self.x, self.velocidade = LARGURA + random.randint(0, 80), velocidade
        tipo = random.random()
        if tipo < 0.45:
            self.largura, self.altura = random.choice((20, 30, 45)), random.choice((35, 50))
            self.y, self.cor = CHAO_Y - self.altura, (200, 50, 50)
        elif tipo < 0.70:
            self.largura, self.altura = 65, 40
            self.y, self.cor = CHAO_Y - self.altura, (160, 20, 20)
        else:
            self.largura, self.altura = 45, 24
            self.y = random.choice((CHAO_Y - 26, CHAO_Y - 46, CHAO_Y - 62, CHAO_Y - 85))
            self.cor = (50, 80, 200)

    def atualizar(self): self.x -= self.velocidade
    def get_rect(self): return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self):
        x, y, w, h = int(self.x), int(self.y), int(self.largura), int(self.altura)
        if self.cor == (50, 80, 200):
            asa_cima = (pygame.time.get_ticks() // 140) % 2 == 0
            pygame.draw.rect(TELA, self.cor, (x, y + 10, 12, 5))
            pygame.draw.rect(TELA, self.cor, (x + 10, y + 7, 22, 11))
            pygame.draw.rect(TELA, self.cor, (x + 32, y + 11, 13, 4))
            pts = [(x + 14, y + 8), (x + 22, y - 8), (x + 28, y + 8)] if asa_cima else [(x + 14, y + 16), (x + 22, y + 28), (x + 28, y + 16)]
            pygame.draw.polygon(TELA, (30, 50, 150), pts)
        else:
            verde = (34, 139, 34) if self.largura < 60 else (20, 100, 20)
            n = 2 if self.largura >= 60 else 1
            lu = w // n
            for idx in range(n):
                cx = x + idx * lu
                tw = max(8, lu // 3)
                tx = cx + (lu - tw) // 2
                pygame.draw.rect(TELA, verde, (tx, y, tw, h))
                pygame.draw.rect(TELA, verde, (cx + 2, y + int(h * 0.35), tx - cx, 5))
                pygame.draw.rect(TELA, verde, (cx + 2, y + int(h * 0.18), 5, int(h * 0.22)))
                pygame.draw.rect(TELA, verde, (tx + tw, y + int(h * 0.45), cx + lu - tx - tw - 2, 5))
                pygame.draw.rect(TELA, verde, (cx + lu - 7, y + int(h * 0.25), 5, int(h * 0.25)))

def eval_genomes(genomes, config):
    global geracao
    geracao += 1
    nets, ge, dinos = [], [], []
    for _, genome in genomes:
        genome.fitness = 0
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        dinos.append(Dinossauro())
        ge.append(genome)

    velocidade_jogo, direcao_vel, indice_zona = 5.0, 1, 2
    centro_zona = LOCAIS_ZONA[indice_zona]
    obstaculos, pontos, clock = [Obstaculo(velocidade_jogo)], 0, pygame.time.Clock()

    while len(dinos) > 0:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if ge:
                    with open("melhor_dino.pkl", "wb") as f:
                        pickle.dump(max(ge, key=lambda g: g.fitness), f)
                pygame.quit()
                quit()

        pontos += 1
        if pontos % 80 == 0:
            velocidade_jogo = max(5.0, min(10.0, velocidade_jogo + 0.5 * direcao_vel))
            if velocidade_jogo in (5.0, 10.0): direcao_vel *= -1

        if pontos % 90 == 0:
            indice_zona = random.choice([idx for idx in range(5) if idx != indice_zona])
            centro_zona = LOCAIS_ZONA[indice_zona]

        gap_min = int(velocidade_jogo * 42 + 240)
        if not obstaculos or obstaculos[-1].x < LARGURA - random.randint(gap_min, gap_min + 260):
            obstaculos.append(Obstaculo(velocidade_jogo))

        for obs in list(obstaculos):
            obs.velocidade = velocidade_jogo
            obs.atualizar()
            if obs.x + obs.largura < 0: obstaculos.remove(obs)

        for i in range(len(dinos) - 1, -1, -1):
            dino = dinos[i]
            dino.atualizar()
            centro_dino = dino.x + dino.largura / 2.0
            fator = max(0.0, min(1.0, 1.0 - abs(centro_dino - centro_zona) / 360.0))
            ge[i].fitness += 0.1 + 0.9 * fator

            proximo_obs = next((obs for obs in obstaculos if obs.x + obs.largura > dino.x), None)
            delta_zona = (centro_zona - centro_dino) / 300.0
            dist_abs = abs(centro_zona - centro_dino) / 300.0

            if proximo_obs:
                prox = max(0.0, 1.0 - max(0.0, proximo_obs.x - dino.x) / 450.0)
                inputs = (prox, (CHAO_Y - proximo_obs.y) / 100.0, proximo_obs.largura / 100.0, velocidade_jogo / 10.0, delta_zona, dist_abs)
            else:
                inputs = (0.0, 0.0, 0.0, velocidade_jogo / 10.0, delta_zona, dist_abs)

            vp, va, ve, vd = nets[i].activate(inputs)
            if ve > 0.5 and vd <= 0.5: dino.mover_esquerda()
            elif vd > 0.5 and ve <= 0.5: dino.mover_direita()

            if vp > 0.5 and not dino.pulando:
                dino.abaixar(False)
                dino.pular()
                if not proximo_obs or (proximo_obs.x - dino.x) > 260: ge[i].fitness -= 2.5
            elif va > 0.5:
                dino.abaixar(True)
                if proximo_obs and proximo_obs.y in (CHAO_Y - 46, CHAO_Y - 62) and not dino.pulando: ge[i].fitness += 0.05
            else:
                dino.abaixar(False)

            if proximo_obs and dino.get_rect().colliderect(proximo_obs.get_rect()):
                ge[i].fitness -= 1
                dinos.pop(i); nets.pop(i); ge.pop(i)

        TELA.fill((245, 245, 245))
        for px in range(20, 395, 3):
            f = max(0.0, min(1.0, 1.0 - abs(px - centro_zona) / 360.0))
            pygame.draw.rect(TELA, (int(255 - 175 * f), int(235 - 25 * f), int(170 - 70 * f)), (px, CHAO_Y, 3, 10))
        pygame.draw.line(TELA, (20, 140, 40), (centro_zona, CHAO_Y - 6), (centro_zona, CHAO_Y + 12), 3)
        for pos in LOCAIS_ZONA: pygame.draw.line(TELA, (120, 120, 120), (pos, CHAO_Y + 10), (pos, CHAO_Y + 15), 2)
        pygame.draw.line(TELA, (100, 100, 100), (0, CHAO_Y), (LARGURA, CHAO_Y), 2)
        pygame.draw.line(TELA, (210, 210, 210), (395, 50), (395, CHAO_Y), 1)

        for obs in obstaculos: obs.desenhar()
        for dino in dinos: dino.desenhar()

        seta = "↑" if direcao_vel == 1 else "↓"
        TELA.blit(FONTE.render(f"Geracao: {geracao}", True, (0, 0, 0)), (10, 10))
        TELA.blit(FONTE.render(f"Vivos: {len(dinos)}", True, (0, 0, 0)), (10, 35))
        TELA.blit(FONTE.render(f"Pontos: {pontos} | Vel: {velocidade_jogo:.1f} {seta} | Zona: {indice_zona + 1}/5", True, (0, 0, 0)), (10, 60))
        pygame.display.flip()

def run(config_path):
    global geracao
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    checkpoints = glob.glob("neat-checkpoint-*")
    if checkpoints:
        ultimo = max(checkpoints, key=lambda x: int(x.split("-")[-1]))
        populacao = neat.Checkpointer.restore_checkpoint(ultimo)
        geracao = populacao.generation
    else:
        populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.Checkpointer(generation_interval=5, filename_prefix="neat-checkpoint-"))
    vencedor = populacao.run(eval_genomes, 500)
    with open("melhor_dino.pkl", "wb") as f: pickle.dump(vencedor, f)

if __name__ == "__main__":
    run(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config-feedforward.txt"))

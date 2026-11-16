import pygame

def criar_textura_cacto(largura=40, altura=70):
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    VERDE_ESCURO = (26, 92, 42)
    VERDE_MEDIO  = (46, 139, 87)
    VERDE_CLARO  = (102, 205, 170)
    ESPINHO      = (235, 245, 220)

    tronco_w = int(largura * 0.35)
    tronco_x = (largura - tronco_w) // 2
    pygame.draw.rect(superficie, VERDE_ESCURO, (tronco_x - 2, 2, tronco_w + 4, altura - 2), border_radius=6)
    pygame.draw.rect(superficie, VERDE_MEDIO, (tronco_x, 4, tronco_w, altura - 4), border_radius=5)
    pygame.draw.rect(superficie, VERDE_CLARO, (tronco_x + 2, 6, 3, altura - 10), border_radius=2)

    braco_esq_y = int(altura * 0.35)
    pygame.draw.rect(superficie, VERDE_ESCURO, (2, braco_esq_y - 12, tronco_x, 16), border_radius=4)
    pygame.draw.rect(superficie, VERDE_MEDIO, (4, braco_esq_y - 10, tronco_x - 2, 12), border_radius=3)
    pygame.draw.rect(superficie, VERDE_ESCURO, (2, braco_esq_y - 25, 12, 25), border_radius=4)
    pygame.draw.rect(superficie, VERDE_MEDIO, (4, braco_esq_y - 23, 8, 21), border_radius=3)

    braco_dir_y = int(altura * 0.45)
    dir_x = tronco_x + tronco_w
    pygame.draw.rect(superficie, VERDE_ESCURO, (dir_x - 2, braco_dir_y - 12, largura - dir_x, 16), border_radius=4)
    pygame.draw.rect(superficie, VERDE_MEDIO, (dir_x, braco_dir_y - 10, largura - dir_x - 4, 12), border_radius=3)
    pygame.draw.rect(superficie, VERDE_ESCURO, (largura - 14, braco_dir_y - 28, 12, 28), border_radius=4)
    pygame.draw.rect(superficie, VERDE_MEDIO, (largura - 12, braco_dir_y - 26, 8, 24), border_radius=3)

    posicoes_espinhos = [
        (tronco_x - 3, 15), (tronco_x + tronco_w + 1, 22),
        (tronco_x - 3, 42), (tronco_x + tronco_w + 1, 50),
        (tronco_x + 5, 18), (tronco_x + 7, 36), (tronco_x + 4, 55)
    ]
    for x, y in posicoes_espinhos:
        pygame.draw.line(superficie, ESPINHO, (x, y), (x + 2, y - 1), 2)

    return superficie

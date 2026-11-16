import pygame

# Matriz pixel-art fiel ao T-Rex do Chrome (22x24 pixels, escalada 2x -> 44x48)
DINO_EM_PE_1 = [
    "...........XXXXXXXX...",
    "..........XXXXXXXXXX..",
    "..........XX.XXXXXXX..",
    "..........XXXXXXXXXX..",
    "..........XXXXXXXXXX..",
    "..........XXXXXXXXXX..",
    "..........XXXXXX......",
    "..........XXXXXXXXX...",
    "X........XXXXXXXX.....",
    "X.......XXXXXXXXX.....",
    "XX.....XXXXXXXXXXXX...",
    "XXX...XXXXXXXXXXX.X...",
    "XXXX.XXXXXXXXXXXX.....",
    "XXXXXXXXXXXXXXXXX.....",
    ".XXXXXXXXXXXXXXXX.....",
    "..XXXXXXXXXXXXXX......",
    "...XXXXXXXXXXXX.......",
    "....XXXXXXXXXX........",
    ".....XXXX.XXXX........",
    ".....XXX...XXX........",
    ".....XX.....XX........",
    ".....XXX....XX........",
    "............XXX.......",
    "......................",
]

DINO_EM_PE_2 = [
    "...........XXXXXXXX...",
    "..........XXXXXXXXXX..",
    "..........XX.XXXXXXX..",
    "..........XXXXXXXXXX..",
    "..........XXXXXXXXXX..",
    "..........XXXXXXXXXX..",
    "..........XXXXXX......",
    "..........XXXXXXXXX...",
    "X........XXXXXXXX.....",
    "X.......XXXXXXXXX.....",
    "XX.....XXXXXXXXXXXX...",
    "XXX...XXXXXXXXXXX.X...",
    "XXXX.XXXXXXXXXXXX.....",
    "XXXXXXXXXXXXXXXXX.....",
    ".XXXXXXXXXXXXXXXX.....",
    "..XXXXXXXXXXXXXX......",
    "...XXXXXXXXXXXX.......",
    "....XXXXXXXXXX........",
    ".....XXXX.XXXX........",
    ".....XXX...XXX........",
    ".....XX.....XXX.......",
    ".....XXX..............",
    "......................",
    "......................",
]

DINO_AGACHADO_1 = [
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "......................XXXXXXXX..",
    "X...................XXXXXXXXXXXX",
    "XX.................XXXXX.XXXXXXX",
    "XXXX..............XXXXXXXXXXXXXX",
    "XXXXXX..........XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ".XXXXXXXXXXXXXXXXXXXXXXXXX......",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXX..",
    "...XXXXXXXXXXXXXXXXXXXXXX.......",
    ".....XXXXXXXXXXXXXXXXXX.........",
    ".......XXXX......XXXX...........",
    ".......XXX........XXX...........",
    ".......XX..........XX...........",
    ".......XXX.........XX...........",
    "...................XXX..........",
    "................................",
    "................................",
    "................................",
]

DINO_AGACHADO_2 = [
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "......................XXXXXXXX..",
    "X...................XXXXXXXXXXXX",
    "XX.................XXXXX.XXXXXXX",
    "XXXX..............XXXXXXXXXXXXXX",
    "XXXXXX..........XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ".XXXXXXXXXXXXXXXXXXXXXXXXX......",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXX..",
    "...XXXXXXXXXXXXXXXXXXXXXX.......",
    ".....XXXXXXXXXXXXXXXXXX.........",
    ".......XXXX......XXXX...........",
    ".......XXX........XXX...........",
    ".......XX..........XXX..........",
    ".......XXX......................",
    "................................",
    "................................",
    "................................",
    "................................",
]

def criar_sprite_dino(matriz, cor, escala=2):
    altura = len(matriz)
    largura = len(matriz[0])
    surf = pygame.Surface((largura * escala, altura * escala), pygame.SRCALPHA)
    cor_borda = (max(0, cor[0] - 45), max(0, cor[1] - 45), max(0, cor[2] - 45))

    for y, linha in enumerate(matriz):
        for x, char in enumerate(linha):
            if char == "X":
                pygame.draw.rect(surf, cor, (x * escala, y * escala, escala, escala))
                # Contorno sutil na borda inferior/direita para dar volume
                if y + 1 < altura and matriz[y + 1][x] == ".":
                    pygame.draw.rect(surf, cor_borda, (x * escala, y * escala + escala - 1, escala, 1))
    return surf

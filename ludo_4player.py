import pygame
import random
import sys

pygame.init()

# ---------------- SETTINGS ----------------
CELL = 40
GRID = 15
WIDTH = CELL * GRID
HEIGHT = CELL * GRID

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ludo 4 Player - Azhar Edition")

font = pygame.font.SysFont(None, 28)

clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

COLORS = {
    "RED": (220,50,50),
    "BLUE": (50,50,220),
    "GREEN": (40,170,40),
    "YELLOW": (230,200,20)
}

# ---------------- PATH (square path) ----------------
path = []

for i in range(1,14):
    path.append((i,7))
for i in range(7,14):
    path.append((13,i))
for i in range(13,0,-1):
    path.append((i,13))
for i in range(13,6,-1):
    path.append((1,i))

# safe cells
safe_cells = [0, 8, 13, 21]

# ---------------- PLAYERS ----------------
players = [
    {"name":"RED", "pos":-1},
    {"name":"BLUE", "pos":-1},
    {"name":"GREEN", "pos":-1},
    {"name":"YELLOW", "pos":-1}
]

current_player = 0
dice_value = 1


# ---------------- FUNCTIONS ----------------

def roll_dice():
    return random.randint(1,6)


def draw_grid():
    for r in range(GRID):
        for c in range(GRID):
            pygame.draw.rect(screen, (230,230,230),
                             (c*CELL, r*CELL, CELL, CELL), 1)


def draw_path():
    for (c,r) in path:
        pygame.draw.rect(screen, (200,200,200),
                         (c*CELL, r*CELL, CELL, CELL))


def draw_tokens():
    for p in players:
        if p["pos"] >= 0 and p["pos"] < len(path):
            c,r = path[p["pos"]]
            pygame.draw.circle(screen, COLORS[p["name"]],
                               (c*CELL+20, r*CELL+20), 15)


def draw_ui():
    text1 = font.render(f"Dice: {dice_value}", True, BLACK)
    text2 = font.render(f"Turn: {players[current_player]['name']}", True, BLACK)

    screen.blit(text1, (20,20))
    screen.blit(text2, (20,50))


def move_player():
    global current_player

    player = players[current_player]

    # home rule
    if player["pos"] == -1:
        if dice_value == 6:
            player["pos"] = 0
    else:
        player["pos"] += dice_value

    # win
    if player["pos"] >= len(path):
        print(player["name"], "WINS 🏆")
        pygame.quit()
        sys.exit()

    # next turn
    current_player = (current_player + 1) % 4


# ---------------- GAME LOOP ----------------
running = True

while running:
    clock.tick(60)
    screen.fill(WHITE)

    draw_grid()
    draw_path()
    draw_tokens()
    draw_ui()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            dice_value = roll_dice()
            move_player()

    pygame.display.update()

pygame.quit()
sys.exit()

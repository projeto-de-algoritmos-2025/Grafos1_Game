import tkinter
import random
from collections import deque

# Tamanho do grid e tiles
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# Classe Tile que representa cada posição da cobrinha/comida
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Janela do Jogo
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Centraliza a janela na tela
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{window_width}x{window_height}+{int((screen_width/2)-(window_width/2))}+{int((screen_height/2)-(window_height/2))}")

# Inicialização
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = []
game_over = False
score = 0
high_score = 0
waiting_to_start = True
paused = False
path = []
use_bfs = True
algorithm_selected = False
obstacles = []  # Lista para armazenar os obstáculos

# Escolha entre BFS e DFS após tela inicial e também durante o jogo
def toggle_algorithm(e):
    global use_bfs
    key = e.keysym.lower()
    if key == "b":
        use_bfs = True
    elif key == "d":
        use_bfs = False

def toggle_pause(e):
    global paused, path
    if not paused and algorithm_selected:
        paused = True
        if use_bfs:
            path = bfs((snake.x, snake.y), (food.x, food.y))
        else:
            path = dfs((snake.x, snake.y), (food.x, food.y))
    else:
        paused = False
        path = []

# Muda a direção da cobrinha
def change_direction(e):
    global velocityX, velocityY, game_over, waiting_to_start, paused, path, algorithm_selected

    if waiting_to_start:
        if e.keysym in ["Up", "Down", "Left", "Right"]:
            waiting_to_start = False
        else:
            return

    if not algorithm_selected:
        toggle_algorithm(e)
        if e.keysym.lower() in ["b", "d"]:
            algorithm_selected = True
        return

    if game_over:
        restart_game()
        return

    if paused:
        paused = False
        path = []

    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, high_score, obstacles
    if game_over or paused or not algorithm_selected:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    for obs in obstacles:
        if snake.x == obs.x and snake.y == obs.y:
            game_over = True
            return

    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        score += 1
        if score > high_score:
            high_score = score
        while True:
            food.x = random.randint(0, COLS - 1) * TILE_SIZE
            food.y = random.randint(0, ROWS - 1) * TILE_SIZE
            if all(food.x != t.x or food.y != t.y for t in snake_body + obstacles) and (food.x != snake.x or food.y != snake.y):
                break
        # Gera obstáculo em posição livre
        while True:
            ox = random.randint(0, COLS - 1) * TILE_SIZE
            oy = random.randint(0, ROWS - 1) * TILE_SIZE
            if all(ox != t.x or oy != t.y for t in snake_body + obstacles) and (ox != snake.x or oy != snake.y) and (ox != food.x or oy != food.y):
                obstacles.append(Tile(ox, oy))
                break

    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    canvas.delete("all")

    if waiting_to_start:
        canvas.create_text(WINDOW_WIDTH/2 + 2, WINDOW_HEIGHT/2 - 80 + 2, font="Arial 28 bold", text="🐍 SNAKE GAME 🐍", fill="gray")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 80, font="Arial 28 bold", text="🐍 SNAKE GAME 🐍", fill="magenta")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text="Bem vindo!", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10, font="Arial 12", text="\n\n\n\nPressione ↑ ↓ ← → para iniciar", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 120, font="Arial 10 italic", 
                           text="\n\nQuer uma dica? Pressione a tecla espaço e veja o menor caminho!", fill="light gray")
        window.after(100, draw)
        return

    if not algorithm_selected:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, font="Arial 18 bold", text="Selecione o algoritmo:", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 16", text="[B] BFS (Busca em Largura)", fill="gray")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30, font="Arial 16", text="[D] DFS (Busca em Profundidade)", fill="gray")
        window.after(100, draw)
        return

    move()

    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='white')
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='green')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='green')

    for obs in obstacles:
        canvas.create_rectangle(obs.x, obs.y, obs.x + TILE_SIZE, obs.y + TILE_SIZE, fill='red')

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10, font="Arial 12", text="\n\n\n\nPressione qualquer tecla para reiniciar", fill="white")
    else:
        canvas.create_text(50, 20, anchor="w", font="Arial 10", text=f"Pontuação atual: {score}", fill="white")
        canvas.create_text(50, 40, anchor="w", font="Arial 10", text=f"Maior Pontuação: {high_score}", fill="white")
        canvas.create_text(WINDOW_WIDTH - 80, 20, font="Arial 10", text=f"Modo: {'BFS' if use_bfs else 'DFS'}", fill="light gray")
        

    if paused:
        for (x, y) in path:
            canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill="gray" if use_bfs else "blue")

    window.after(100, draw)

def restart_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score, paused, path, algorithm_selected, obstacles

    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
    food = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0
    paused = False
    path = []
    algorithm_selected = False
    obstacles = []

def bfs(start, goal):
    directions = [(0, -TILE_SIZE), (0, TILE_SIZE), (-TILE_SIZE, 0), (TILE_SIZE, 0)]
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(start)
    obstacle_positions = {(tile.x, tile.y) for tile in snake_body + obstacles}

    while queue:
        current, current_path = queue.popleft()
        if current == goal:
            return current_path

        for dx, dy in directions:
            new_x = current[0] + dx
            new_y = current[1] + dy
            next_pos = (new_x, new_y)

            if 0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT and next_pos not in visited and next_pos not in obstacle_positions:
                visited.add(next_pos)
                queue.append((next_pos, current_path + [next_pos]))
    return []

def dfs(start, goal):
    directions = [(0, -TILE_SIZE), (0, TILE_SIZE), (-TILE_SIZE, 0), (TILE_SIZE, 0)]
    stack = [(start, [])]
    visited = set()
    visited.add(start)
    obstacle_positions = {(tile.x, tile.y) for tile in snake_body + obstacles}

    while stack:
        current, current_path = stack.pop()
        if current == goal:
            return current_path

        for dx, dy in directions:
            new_x = current[0] + dx
            new_y = current[1] + dy
            next_pos = (new_x, new_y)

            if 0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT and next_pos not in visited and next_pos not in obstacle_positions:
                visited.add(next_pos)
                stack.append((next_pos, current_path + [next_pos]))
    return []

# Bind de teclas
window.bind("<KeyRelease>", change_direction)
window.bind("<space>", toggle_pause)
window.bind("b", toggle_algorithm)
window.bind("d", toggle_algorithm)

# Inicia o jogo
draw()
window.mainloop()


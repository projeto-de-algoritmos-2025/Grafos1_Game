import tkinter
import random  
from collections import deque

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS #25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS #25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Janela do Jogo
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#Centro
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#Formato "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#Inicialização
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) 
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = []
game_over = False
score = 0
waiting_to_start = True 
paused = False 
path = []

def toggle_pause(e):
    global paused, path
    if not paused:
        paused = True
        path = bfs((snake.x, snake.y), (food.x, food.y))
    else:
        paused = False
        path = []

#Loop do jogo
def change_direction(e):

    global velocityX, velocityY, game_over, waiting_to_start, paused, path
    
    if waiting_to_start:
        if e.keysym in ["Up", "Down", "Left", "Right"]:
            waiting_to_start = False  
        else:
            return  
    
    if (game_over):
        restart_game()
        return
    
    if paused:
        paused = False
        path = []

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
        
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0


def move():
    global snake, food, snake_body, game_over, score
    if (game_over) or paused:
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    #Quando houver colisão
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    #Atualiza somando ao corpo 
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")
    
    if waiting_to_start:
        # Título com sombra
        canvas.create_text(WINDOW_WIDTH/2 + 2, WINDOW_HEIGHT/2 - 80 + 2,
                       font="Arial 28 bold", text="🐍 SNAKE GAME 🐍", fill="gray")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 80,
                       font="Arial 28 bold", text="🐍 SNAKE GAME 🐍", fill="magenta")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = "Bem vindo!",  fill = "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10, font = "Arial 12", text = "\n\n\n\nPressione ↑ ↓ ← → para iniciar", fill = "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 120, font = "Arial 10 italic", 
                       text = "\n\nQuer uma dica? Pressione a tecla \nespaço e veja o menor caminho!", 
                       fill = "light gray")
        window.after(100, draw)
        return


    #Comida
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #Cobra
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = 'lime green')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'lime green')

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10, font = "Arial 12", text = "\n\n\n\nPressione qualquer tecla para reiniciar", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")

    if paused:
        for (x, y) in path:
            canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill="gray")


    window.after(100, draw) #Chama o draw a cada 100ms -> 10 frames por segundo

def restart_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score, paused, path

    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
    food = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0
    paused = False
    path = []


def bfs(start, goal):
    directions = [(0, -TILE_SIZE), (0, TILE_SIZE), (-TILE_SIZE, 0), (TILE_SIZE, 0)]
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(start)

    obstacles = {(tile.x, tile.y) for tile in snake_body}

    while queue:
        current, current_path = queue.popleft()
        if current == goal:
            return current_path

        for dx, dy in directions:
            new_x = current[0] + dx
            new_y = current[1] + dy
            next_pos = (new_x, new_y)

            if (0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT and
                next_pos not in visited and next_pos not in obstacles):
                visited.add(next_pos)
                queue.append((next_pos, current_path + [next_pos]))

    return [] 


draw()
window.bind("<KeyRelease>", change_direction) #Muda a direção
window.bind("<space>", toggle_pause) #Pausa e Calcula menor caminho por BFS
window.mainloop() #Acompanha eventos 


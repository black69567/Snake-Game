import tkinter
import random  

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS  # 25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS  # 25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Janela do jogo
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Centralizar a janela
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# Formato "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Inicializar o jogo
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)  # Tile único, a cabeça da cobra
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = []  # Tiles múltiplos, corpo da cobra
game_over = False
score = 0
speed = 150  # Velocidade inicial (150ms de atraso)

# Laço principal do jogo
def change_direction(e):  # e = evento
    global velocityX, velocityY, game_over
    if game_over:
        return  # Editar aqui para redefinir variáveis do jogo e jogar novamente

    # Setas direcionais e teclas WASD
    if (e.keysym in ["Up", "w"] and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym in ["Down", "s"] and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym in ["Left", "a"] and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym in ["Right", "d"] and velocityX != -1):
        velocityX = 1
        velocityY = 0

def increase_speed(e):
    """Aumenta a velocidade quando Shift é pressionado."""
    global speed
    speed = 75  # Velocidade mais rápida

def reset_speed(e):
    """Redefine a velocidade ao soltar Shift."""
    global speed
    speed = 150  # Velocidade normal

def move():
    global snake, food, snake_body, game_over, score
    if game_over:
        return

    # Verificar colisão com as bordas
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    # Verificar colisão com o próprio corpo
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Colisão com a comida
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    # Atualizar o corpo da cobra
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score, speed
    move()

    canvas.delete("all")

    # Desenhar a comida
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Desenhar a cabeça da cobra
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='green')

    # Desenhar o corpo da cobra
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='green')

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Fim de jogo: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Pontos: {score}", fill="white")

    # Ajustar a velocidade dinamicamente
    window.after(speed, draw)

draw()
window.bind("<KeyRelease>", change_direction)  # Detectar mudanças de direção
window.bind("<KeyPress-Shift_L>", increase_speed)  # Aumentar a velocidade ao pressionar Shift
window.bind("<KeyRelease-Shift_L>", reset_speed)  # Redefinir a velocidade ao soltar Shift
window.mainloop()  # Manter a janela rodando

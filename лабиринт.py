import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 3
MAX_DEPTH = 20
FPS = 60
MINIMAP_SCALE = 5  # Масштаб миникарты

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Maze Game")
clock = pygame.time.Clock()

# Генерация лабиринта
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_passages(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                maze[cx + dx][cy + dy] = 0
                maze[nx][ny] = 0
                carve_passages(nx, ny)

    maze[1][1] = 0
    carve_passages(1, 1)
    maze[rows - 2][cols - 2] = 0
    return maze

# Игрок
class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0.05
        self.turn_speed = 0.03
        self.strafe_speed = 0.04
        self.step = 0  # Для анимации

    def move(self, maze):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y
        moved = False

        if keys[pygame.K_w]:
            new_x += math.cos(self.angle) * self.speed
            new_y += math.sin(self.angle) * self.speed
            moved = True
        if keys[pygame.K_s]:
            new_x -= math.cos(self.angle) * self.speed
            new_y -= math.sin(self.angle) * self.speed
            moved = True
        if keys[pygame.K_a]:
            new_x += math.sin(self.angle) * self.strafe_speed
            new_y -= math.cos(self.angle) * self.strafe_speed
            moved = True
        if keys[pygame.K_d]:
            new_x -= math.sin(self.angle) * self.strafe_speed
            new_y += math.cos(self.angle) * self.strafe_speed
            moved = True

        # Поворот камеры
        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed

        # Проверка на столкновения с лабиринтом
        if 0 <= int(new_y) < len(maze) and 0 <= int(new_x) < len(maze[0]) and maze[int(new_y)][int(new_x)] == 0:
            self.x, self.y = new_x, new_y
            if moved:
                self.step += 1  # Увеличиваем шаг при движении

# Рендеринг 3D вида
def render_3d_view(player, maze):
    for column in range(WIDTH):
        angle = player.angle - FOV / 2 + column / WIDTH * FOV
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        for depth in range(1, MAX_DEPTH):
            target_x = player.x + cos_a * depth
            target_y = player.y + sin_a * depth
            if int(target_y) >= len(maze) or int(target_x) >= len(maze[0]) or maze[int(target_y)][int(target_x)] == 1:
                color_intensity = 255 / (1 + depth * depth * 0.1)
                shade = (color_intensity, color_intensity, color_intensity)
                wall_height = HEIGHT / (depth * math.cos(angle - player.angle))
                pygame.draw.rect(screen, shade, (column, HEIGHT // 2 - wall_height // 2, 1, wall_height))
                break

# Рендеринг миникарты
def render_minimap(player, maze, finish):
    rows, cols = len(maze), len(maze[0])
    for y in range(rows):
        for x in range(cols):
            color = BLACK if maze[y][x] == 1 else WHITE
            pygame.draw.rect(
                screen,
                color,
                (x * MINIMAP_SCALE, y * MINIMAP_SCALE, MINIMAP_SCALE, MINIMAP_SCALE),
            )
    # Положение игрока
    pygame.draw.circle(
        screen,
        RED,
        (int(player.x * MINIMAP_SCALE), int(player.y * MINIMAP_SCALE)),
        MINIMAP_SCALE // 2,
    )
    # Положение синего квадрата
    pygame.draw.rect(
        screen,
        BLUE,
        (finish[0] * MINIMAP_SCALE, finish[1] * MINIMAP_SCALE, MINIMAP_SCALE, MINIMAP_SCALE),
    )

# Отображение шага игрока (анимация)
def render_step(player):
    step_phase = (player.step // 10) % 2  # Два кадра анимации
    step_color = GRAY if step_phase == 0 else BLUE
    pygame.draw.rect(screen, step_color, (WIDTH - 50, HEIGHT - 50, 30, 30))

# Проверка на победу
def check_win(player, goal):
    return int(player.x) == goal[0] and int(player.y) == goal[1]

# Проверка на проигрыш
def check_lose(player, finish):
    return int(player.x) == finish[0] and int(player.y) == finish[1]

# Основная функция
def main():
    rows, cols = 20, 20
    maze = generate_maze(rows, cols)
    player = Player(1.5, 1.5, 0)
    goal = (cols - 2, rows - 2)  # Координаты выхода
    finish = (cols // 2, rows // 2)  # Координаты синего квадрата

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.move(maze)

        # Проверка на победу
        if check_win(player, goal):
            print("Вы выиграли!")
            running = False

        # Проверка на проигрыш
        if check_lose(player, finish):
            print("Игра окончена!")
            running = False

        # Рендеринг
        screen.fill(BLACK)
        render_3d_view(player, maze)
        render_minimap(player, maze, finish)  # Рендеринг миникарты
        render_step(player)  # Отображение анимации шага

        # Отображение выхода
        exit_x = goal[0] + 0.5
        exit_y = goal[1] + 0.5
        exit_screen_x = int((exit_x / cols) * WIDTH)
        exit_screen_y = int((exit_y / rows) * HEIGHT)
        pygame.draw.circle(screen, GREEN, (exit_screen_x, exit_screen_y), 5)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

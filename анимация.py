import pygame
import math
import random
import webbrowser

def main():
    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    pygame.display.set_caption("Анимация логотипа Amazon")

    # Цвета
    BLACK = (0, 0, 0)
    AMAZON_ORANGE = (255, 153, 0)
    WHITE = (255, 255, 255)
    RAINBOW_COLORS = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0),
        (0, 0, 255), (75, 0, 130), (148, 0, 211)
    ]

    # Шрифт
    font_large = pygame.font.SysFont("Arial", 80)
    font_small = pygame.font.SysFont("Arial", 30)

    # Переменные для анимации
    circle_radius = 50
    circle_center = (WIDTH // 2, HEIGHT // 2 - 50)
    circle_angle = 0
    alpha = 0
    start_loading = False
    start_time = pygame.time.get_ticks()

    # Снегопад
    snowflakes = [{"x": random.randint(0, WIDTH), "y": random.randint(-HEIGHT, 0), "radius": random.randint(2, 5), "speed": random.uniform(1, 3)} for _ in range(100)]

    running = True
    while running:
        screen.fill(BLACK)
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Снегопад анимация
        for snowflake in snowflakes:
            pygame.draw.circle(screen, WHITE, (int(snowflake["x"]), int(snowflake["y"])), snowflake["radius"])
            snowflake["y"] += snowflake["speed"]
            if snowflake["y"] > HEIGHT:
                snowflake["y"] = random.randint(-50, -10)
                snowflake["x"] = random.randint(0, WIDTH)

        # Анимация текста "AXLEBOLT"
        if elapsed_time < 1.5:
            alpha = min(alpha + 5, 255)
        elif elapsed_time < 2.5:
            alpha = 255
        elif elapsed_time < 3:
            alpha = max(alpha - 5, 0)
        else:
            alpha = 0
            start_loading = True

        # Показ названия студии
        if not start_loading:
            studio_text = font_large.render("AXLEBOLT", True, WHITE)
            studio_text.set_alpha(alpha)
            screen.blit(studio_text, (WIDTH // 2 - studio_text.get_width() // 2, HEIGHT // 2 - studio_text.get_height() // 2))
        else:
            # Анимация круга
            num_segments = len(RAINBOW_COLORS)
            for i, color in enumerate(RAINBOW_COLORS):
                angle = circle_angle + (i / num_segments) * 2 * math.pi
                x = circle_center[0] + circle_radius * math.cos(angle)
                y = circle_center[1] + circle_radius * math.sin(angle)
                pygame.draw.circle(screen, color, (int(x), int(y)), 10)
            circle_angle += (2 * math.pi / 300) * 0.45

            # Текст "Загрузка приложения"
            loading_text = font_small.render("Загрузка приложения", True, WHITE)
            screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 + 50))

            # Прогресс загрузки
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 20), 2)
            progress_width = min((elapsed_time - 3) / 10 * 300, 300)
            pygame.draw.rect(screen, AMAZON_ORANGE, (WIDTH // 2 - 150, HEIGHT // 2 + 100, progress_width, 20))

            # Процент загрузки
            percentage = int((progress_width / 300) * 100)
            percentage_text = font_small.render(f"{percentage}%", True, WHITE)
            screen.blit(percentage_text, (WIDTH // 2 + 160, HEIGHT // 2 + 95))

            # Если загрузка завершена
            if percentage == 100:
                pygame.time.delay(1000)
                running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # Окно с кнопками
    show_buttons(screen, WIDTH, HEIGHT, AMAZON_ORANGE, WHITE, snowflakes)

def show_buttons(screen, WIDTH, HEIGHT, button_color, text_color, snowflakes):
    button_font = pygame.font.SysFont("Arial", 40)
    button_1_text = button_font.render("Кнопка 1", True, text_color)
    button_2_text = button_font.render("Кнопка 2", True, text_color)
    button_3_text = button_font.render("Выход", True, text_color)

    button_1_rect = pygame.Rect(WIDTH // 8 - 100, HEIGHT // 3 - 50, 200, 50)
    button_2_rect = pygame.Rect(WIDTH // 8 - 100, HEIGHT // 2 - 50, 200, 50)
    button_3_rect = pygame.Rect(WIDTH // 8 - 100, 2 * HEIGHT // 3 - 50, 200, 50)

    # Загрузка изображения рекламы
    ad_image = pygame.image.load("C:\\Users\\Egor\\PycharmProjects\\tree\\photo_2024-12-13_19-33-43.jpg")
    ad_image = pygame.transform.scale(ad_image, (400, 500))
    ad_rect = ad_image.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2))

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Снегопад анимация (в 4 раза медленнее)
        for snowflake in snowflakes:
            pygame.draw.circle(screen, text_color, (int(snowflake["x"]), int(snowflake["y"])), snowflake["radius"])
            snowflake["y"] += snowflake["speed"] * 0.25  # Уменьшение скорости
            if snowflake["y"] > HEIGHT:
                snowflake["y"] = random.randint(-50, -10)
                snowflake["x"] = random.randint(0, WIDTH)

        pygame.draw.rect(screen, button_color, button_1_rect)
        pygame.draw.rect(screen, button_color, button_2_rect)
        pygame.draw.rect(screen, button_color, button_3_rect)

        screen.blit(button_1_text, (WIDTH // 8 - 75, HEIGHT // 3 - 40))
        screen.blit(button_2_text, (WIDTH // 8 - 75, HEIGHT // 2 - 40))
        screen.blit(button_3_text, (WIDTH // 8 - 75, 2 * HEIGHT // 3 - 40))

        # Отображение изображения рекламы
        screen.blit(ad_image, ad_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_1_rect.collidepoint(mouse_pos):
                    print("Нажата Кнопка 1")
                if button_2_rect.collidepoint(mouse_pos):
                    print("Нажата Кнопка 2")
                if button_3_rect.collidepoint(mouse_pos):
                    running = False
                if ad_rect.collidepoint(mouse_pos):
                    webbrowser.open("https://disk.yandex.ru/d/Vf_Mxza6GfnI9g")

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
# дописать увеличь еще больше картинку , над ней добавь небольшую надпись "реклама" и под картинкой добавь надпись "Реклама"
# и объеденить

import pygame
import webbrowser
import random
import math

# Инициализация pygame
pygame.init()


def create_gradient_surface(width, height, color1, color2):
    """Создает градиентный фон"""
    gradient_surface = pygame.Surface((width, height))
    for y in range(height):
        color = (
            int(color1[0] + (color2[0] - color1[0]) * y / height),
            int(color1[1] + (color2[1] - color1[1]) * y / height),
            int(color1[2] + (color2[2] - color1[2]) * y / height)
        )
        pygame.draw.line(gradient_surface, color, (0, y), (width, y))
    return gradient_surface


def show_buttons(screen, WIDTH, HEIGHT, button_color, text_color):
    """Основной интерфейс с кнопками и анимацией"""
    button_font = pygame.font.SysFont("Arial", 40)
    ad_font = pygame.font.SysFont("Arial", 30)

    # Кнопки с текстом
    button_1_text = button_font.render("Начни здесь", True, text_color)
    button_2_text = button_font.render("Подробнее", True, text_color)
    button_3_text = button_font.render("Выход", True, text_color)

    # Прямоугольники кнопок
    button_1_rect = pygame.Rect(WIDTH // 8 - 100, HEIGHT // 3 - 50, 250, 60)
    button_2_rect = pygame.Rect(WIDTH // 8 - 100, HEIGHT // 2 - 50, 250, 60)
    button_3_rect = pygame.Rect(WIDTH // 8 - 100, 2 * HEIGHT // 3 - 50, 250, 60)

    # Загрузка и обработка изображения рекламы
    ad_image = pygame.image.load("C:\\Users\\Egor\\PycharmProjects\\tree\\photo_2024-12-13_19-33-43.jpg")
    ad_image = pygame.transform.scale(ad_image, (600, 750))
    ad_rect = ad_image.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2))

    # Тексты для рекламы
    ad_title_text = ad_font.render("Хотите заказывать быстрее и удобнее? Нажмите на картинку!", True, text_color)
    ad_bottom_text = ad_font.render("Скачайте наше приложение и наслаждайтесь покупками!", True, text_color)

    ad_title_rect = ad_title_text.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2 - ad_image.get_height() // 2 - 40))
    ad_bottom_rect = ad_bottom_text.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2 + ad_image.get_height() // 2 + 40))

    # Снегопад
    snowflakes = [{"x": random.randint(0, WIDTH), "y": random.randint(-HEIGHT, 0), "radius": random.randint(2, 5),
                   "speed": random.uniform(1, 3)} for _ in range(100)]

    # Градиентный фон
    gradient_surface = create_gradient_surface(WIDTH, HEIGHT, (50, 50, 255), (100, 100, 255))

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Отображаем градиентный фон
        screen.blit(gradient_surface, (0, 0))

        # Снегопад анимация
        for snowflake in snowflakes:
            pygame.draw.circle(screen, text_color, (int(snowflake["x"]), int(snowflake["y"])), snowflake["radius"])
            snowflake["y"] += snowflake["speed"] * 0.25
            if snowflake["y"] > HEIGHT:
                snowflake["y"] = random.randint(-50, -10)
                snowflake["x"] = random.randint(0, WIDTH)

        # Кнопки с эффектами наведения
        mouse_pos = pygame.mouse.get_pos()
        for button_rect, button_text, text_pos in [
            (button_1_rect, button_1_text, (WIDTH // 8 - 90, HEIGHT // 3 - 40)),
            (button_2_rect, button_2_text, (WIDTH // 8 - 90, HEIGHT // 2 - 40)),
            (button_3_rect, button_3_text, (WIDTH // 8 - 90, 2 * HEIGHT // 3 - 40))
        ]:
            pygame.draw.rect(screen, button_color, button_rect, border_radius=15)  # Круглые углы
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), button_rect, border_radius=15)  # При наведении меняется цвет
            screen.blit(button_text, text_pos)

        # Отображение текста над картинкой
        screen.blit(ad_title_text, ad_title_rect)

        # Отображение изображения рекламы
        screen.blit(ad_image, ad_rect)

        # Отображение текста под картинкой
        screen.blit(ad_bottom_text, ad_bottom_rect)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1_rect.collidepoint(mouse_pos):
                    print("Нажата Кнопка 1")
                    start_chess_game()  # Запуск шахматной игры
                if button_2_rect.collidepoint(mouse_pos):
                    print("Нажата Кнопка 2")
                if button_3_rect.collidepoint(mouse_pos):
                    running = False
                if ad_rect.collidepoint(mouse_pos):
                    webbrowser.open("https://disk.yandex.ru/d/Vf_Mxza6GfnI9g")

        pygame.display.flip()

    pygame.quit()
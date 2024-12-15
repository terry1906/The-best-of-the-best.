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
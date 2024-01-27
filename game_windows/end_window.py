import pygame


def start_final_window(given_score):
    given_score = str(given_score)
    # Инициализация Pygame
    pygame.init()

    # Установка размеров окна
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Игра")

    # Загрузка изображений для кнопки "New Game" и фона
    new_game_button_img = pygame.image.load("data/assets/new_game_button.png")

    # Загрузка значения рекорда из файла
    with open("data/game_data/record.txt", "r") as file:
        record_value = int(file.read())

    # Создание текстового объекта для отображения рекорда
    font = pygame.font.Font(None, 36)
    text = font.render("Рекорд: " + str(record_value), True, (0, 0, 0))
    your_score_text = font.render("Ваш счёт: " + given_score, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width / 2, 50))
    your_score_text_rect = your_score_text.get_rect(center=(screen_width / 2, 100))

    # Создание класса для кнопок
    class Button(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    # Создание группы спрайтов для кнопок
    buttons = pygame.sprite.Group()
    new_game_button = Button(
        new_game_button_img, screen_width / 2 - new_game_button_img.get_width() / 2, 300
    )
    buttons.add(new_game_button)

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если произошло нажатие на кнопку "New Game"
                if new_game_button.rect.collidepoint(event.pos):
                    return True

        # Очистка экрана и отображение фона
        screen.fill(pygame.Color(186, 229, 240))
        # Отрисовка текста рекорда
        screen.blit(text, text_rect)
        screen.blit(your_score_text, your_score_text_rect)
        # Отрисовка всех кнопок
        buttons.draw(screen)

        # Обновление окна
        pygame.display.flip()

    # Завершение работы Pygame
    pygame.quit()

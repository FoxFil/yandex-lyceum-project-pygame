import pygame
from game_windows.game import start_the_game


def start_starting_window():
    # Инициализация Pygame
    pygame.init()

    # Установка размеров окна
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Игра")

    # Загрузка изображения для кнопки "начать игру"
    start_button_img = pygame.image.load("data/assets/start_button.png")

    # Загрузка изображения для спрайта игрока (если нужно)
    # player_img = pygame.image.load('player_sprite.png')

    # Загрузка значения рекорда из файла
    with open("data/game_data/record.txt", "r") as file:
        record_value = int(file.read())

    # Создание текстового объекта для отображения рекорда
    font = pygame.font.Font(None, 36)
    text = font.render("Рекорд: " + str(record_value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width / 2, 50))

    # Создание класса для кнопок
    class Button(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    # Создание группы спрайтов для кнопок
    buttons = pygame.sprite.Group()
    start_button = Button(
        start_button_img, screen_width / 2 - start_button_img.get_width() / 2, 300
    )
    buttons.add(start_button)

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если произошло нажатие на кнопку "начать игру"
                if start_button.rect.collidepoint(event.pos):
                    print("button pressed")
                    return start_the_game()
                # Здесь можно добавить логику для начала игры

        # Очистка экрана
        screen.fill(pygame.Color(186, 229, 240))
        # Отрисовка текста рекорда
        screen.blit(text, text_rect)
        # Отрисовка всех кнопок
        buttons.draw(screen)

        # Обновление окна
        pygame.display.flip()

    # Завершение работы Pygame
    pygame.quit()

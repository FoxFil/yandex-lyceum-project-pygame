import pygame
from game_windows.game import start_the_game


def start_starting_window():

    pygame.init()


    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Игра")

    # картинки
    start_button_img = pygame.image.load("data/assets/start_button.png")

    # рекорд
    with open("data/game_data/record.txt", "r") as file:
        record_value = int(file.read())

    # текстики
    font = pygame.font.Font(None, 36)
    text = font.render("Рекорд: " + str(record_value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width / 2, 50))

    # кнопка
    class Button(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    # спрайты
    buttons = pygame.sprite.Group()
    start_button = Button(
        start_button_img, screen_width / 2 - start_button_img.get_width() / 2, 300
    )
    buttons.add(start_button)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # если нажали на кнопку
                if start_button.rect.collidepoint(event.pos):
                    print("button pressed")
                    return start_the_game()


        screen.fill(pygame.Color(186, 229, 240))

        screen.blit(text, text_rect)

        buttons.draw(screen)


        pygame.display.flip()


    pygame.quit()

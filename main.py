import pygame
import sys
import settings
import klases
import graphics


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Baigiamasis Gyvatukas")

sound_bite = pygame.mixer.Sound("Bite.mp3")
sound_background = pygame.mixer.music.load("background_sound.mp3")
pygame.mixer.music.play()

snake = klases.Snake()
food = klases.Food(snake)

leaderboard = klases.load_leaderboard()
last_player_name = ""

game_state = settings.MENU

auto_move = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if game_state == settings.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                start_button_rect = start_button.get_rect(topleft=(settings.WIDTH // 2 - start_button.get_width() // 2, settings.HEIGHT // 2 - 50))
                leaderboard_button_rect = leaderboard_button.get_rect(topleft=(settings.WIDTH // 2 - leaderboard_button.get_width() // 2, settings.HEIGHT // 2))
                exit_button_rect = exit_button.get_rect(topleft=(settings.WIDTH // 2 - exit_button.get_width() // 2, settings.HEIGHT - 50))
                checkbox_rect = checkbox.get_rect(topright=(settings.WIDTH - settings.GRID_SIZE - 10, settings.GRID_SIZE + 10))
                if klases.is_button_clicked(start_button_rect, pos):
                    if not auto_move:
                        game_state = settings.NAME_INPUT
                    else:
                        game_state = settings.GAME
                if klases.is_button_clicked(exit_button_rect, pos):
                    pygame.quit()
                    sys.exit()
                if klases.is_button_clicked(leaderboard_button_rect, pos):
                    game_state = settings.LEADERBOARD
                if klases.is_button_clicked(checkbox_rect, pos):
                    auto_move = not auto_move

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not auto_move:
                    game_state = settings.NAME_INPUT
                else:
                    game_state = settings.GAME

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                game_state = settings.LEADERBOARD

        elif game_state == settings.GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_s and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_a and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_d and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        elif game_state == settings.LEADERBOARD:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                game_state = settings.MENU
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                back_text_rect = back_text.get_rect(topleft=(settings.WIDTH // 2 - back_text.get_width() // 2, settings.HEIGHT - 50))
                if back_text_rect.collidepoint(pos):
                    game_state = settings.MENU

        elif game_state == settings.NAME_INPUT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_state = settings.GAME
                elif event.key == pygame.K_BACKSPACE:
                    if snake.player_name:
                        snake.player_name = snake.player_name[:-1]
                        last_player_name = last_player_name[:-1]
                elif event.unicode.isprintable():
                    if last_player_name != "":
                        last_player_name = ""
                        snake.player_name = ""
                    snake.player_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                input_text, input_text_position = graphics.game_state_name_input(snake.player_name)
                click_rect = pygame.Rect(input_text_position[0], input_text_position[1], input_text.get_width(), input_text.get_height())
                if klases.is_button_clicked(click_rect, pos):
                    game_state = settings.GAME

    if game_state == settings.GAME:
        if auto_move:
            snake.move_towards_food(food.position)
            snake.move(food.position, auto_move=True)
        else:
            snake.move(food.position)

        if snake.check_collision():
            game_state = settings.MENU
            leaderboard.add_score(snake.player_name, snake.score)
            klases.save_leaderboard(leaderboard)
            last_player_name = snake.player_name
            snake = klases.Snake()
            food = klases.Food(snake)

        if snake.body[0] == food.position:
            sound_bite.play()
            snake.score += 1
            snake.grow()
            food.position = food.generate_position(snake)

    screen.blit(graphics.background, (0, 0))

    if game_state == settings.MENU:
        title_text, start_button, leaderboard_button, exit_button, checkbox, checkbox_rect = graphics.game_state_menu(auto_move)
    elif game_state == settings.NAME_INPUT:
        if last_player_name != "":
            snake.player_name = last_player_name
        graphics.game_state_name_input(snake.player_name)
    elif game_state == settings.GAME:
        snake.draw(screen)
        food.draw(screen)
        graphics.game_state_game(snake.player_name, snake.score, auto_move)
    elif game_state == settings.LEADERBOARD:
        back_text_position, back_text = graphics.game_state_leaderboard(leaderboard)
        graphics.game_state_leaderboard(leaderboard)

    pygame.display.flip()
    clock.tick(10)

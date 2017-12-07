''''
Snake game.
Authors:
Taiha Greenfield, Deja Jones, Caetia Short
'''


import pygame
import random
import sys

# The game grid contains this many cells in the x direction. A piece of food or a segment of the snake takes up one cell.
GRID_WIDTH = 30
# The game grid contains this many cells in the y direction. A piece of food or a segment of the snake takes up one cell.
GRID_HEIGHT = 30
# The height and width of each square cell in pixels.
PIXELS_IN_CELL = 20
# The width of the game grid in pixels.
GRID_WIDTH_PIXELS = PIXELS_IN_CELL * GRID_WIDTH
# The height of the game grid in pixels.
GRID_HEIGHT_PIXELS = PIXELS_IN_CELL * GRID_HEIGHT
# The initial length of the snake. Before eating any food, the snake contains this many segments.
INITIAL_SNAKE_LENGTH = 10

# Each of these directions contains a 2-tuple representing delta-x and delta-y for moving in that direction.
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)

# Background color of the snake grid.
COLOR_BACKGROUND = (74, 183, 73)  # rgb color for white
# This is the color of the snake's head. 
COLOR_SNAKE_HEAD = (197, 25, 126)      # rgb color for red
# This is the color of the rest of the snake.
COLOR_SNAKE = (207, 81, 159)           # rgb color for green
# This is the color for the snake's food.
COLOR_FOOD = (67, 189, 217)          # rgb color for orange
# This is the color for the game over text.
COLOR_GAME_OVER_TEXT = (0, 0, 0)    # rgb color for black

def get_direction(previous_direction, event_key):
    """Return the new direction of the snake: one of DIRECTION_{LEFT,RIGHT,UP,DOWN}.
    previous_direction - the previous direction of the snake; one of DIRECTION_{LEFT,RIGHT,UP,DOWN} 
    event_key - the event that the user pressed; one of https://www.pygame.org/docs/ref/key.html
    If event_key does not correspond with any of the arrows keys, return previous_direction.
    """
    if event_key == pygame.K_LEFT:
        if previous_direction == DIRECTION_RIGHT:
            return previous_direction
        else:
            return DIRECTION_LEFT
    elif event_key == pygame.K_UP:
        if previous_direction == DIRECTION_DOWN:
            return previous_direction
        else:
            return DIRECTION_UP
    elif event_key == pygame.K_RIGHT:
        if previous_direction == DIRECTION_LEFT:
            return previous_direction
        else:
            return DIRECTION_RIGHT
    elif event_key == pygame.K_DOWN:
        if previous_direction == DIRECTION_UP:
            return previous_direction
        else:
            return DIRECTION_DOWN
    return previous_direction

def create_food_position():
    """Returns a random 2-tuple in the grid where the food should be located.
    The first element is the x position. Must be an int between 0 and GRID_WIDTH - 1, inclusively.
    The second element is the y position. Must be an int between 0 and GRID_HEIGHT - 1, inclusively.
    """
    x = random.randrange(0, GRID_WIDTH - 1)
    y = random.randrange(0, GRID_HEIGHT - 1)
    position = (x, y)
    return position
    

def snake_ate_food(snake, food):
    """Returns whether food was eaten by the snake.
    snake - list of 2-tuples representing the positions of each snake segment
    food - 2-tuple representing the position in the grid of the food
    This function should return True if the head of the snake is in the same position as food.
    """
    if snake[0] == food:
        return True
    return False

def snake_ran_out_of_bounds(snake):
    """Returns whether the snake has ran off one of the four edges of the grid.
    snake - list of 2-tuples representing the positions of each snake segment
    Note that the grid is GRID_WIDTH cells wide and GRID_HEIGHT cells high.
    """
    if snake[0][0] < 0 or snake[0][0] > GRID_WIDTH - 1:
        return True
    if snake[0][1] < 0 or snake[0][1] > GRID_HEIGHT - 1:
        return True   
    return False

def snake_intersected_body(snake):
    """Returns whether the snake has ran into itself.
    snake - list of 2-tuples representing the positions of each snake segment
    The snake ran into itself if the position of the head is the same as the position
    of any of its body segments.
    """
    for body in range(1, len(snake)):
        if snake[body] == snake[0]:
            return True
    return False

def get_score(snake):
    """Returns the current score of the game.
    snake - list of 2-tuples representing the positions of each snake segment
    The user earns 10 points for each of the segments in the snake.
    For example, if the snake has 25 segments, the score is 250.
    """
    return len(snake) * 10

def get_game_over_text(score):
    """Returns the text to draw on the screen after the game is over.
    This text should contain 'Game Over' as well as the score.
    score - integer representing the current score of the game.
    """
    game_over = 'Game Over ' + str(score)
    return game_over

def get_snake_speed(snake):
    """Return the number of cells the snake should travel in one second.
    snake - list of 2-tuples representing the positions of each snake segment
    The speed at the beginning of the game should be 5. Once the snake has eaten 10 pieces of food,
    the speed of the game should increase (by how much is up to you).
    """
    return len(snake)//2 

def move_snake(snake, direction, food):
    """Moves the snake one space in the direction specified and returns whether food was eaten.
    The snake moves by removing the last segment and added a new head to the beginning of the snake list.
    If the snake ate the food, the last segment is not removed, so the snake grows by a single segment.
    Do not edit this function.
    """
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    snake.insert(0, new_head)
    ate_food = snake_ate_food(snake, food)
    if not ate_food:
        snake.pop()
    return ate_food

def get_initial_snake():
    """Returns a list of 2-tuples representing the initial positions of the snake segments.
    The snake starts with its head in the middle of the grid, extending to the left.
    Do not edit this function.
    """
    snake = []
    head = (GRID_HEIGHT // 2, GRID_WIDTH // 2)
    snake.append(head)
    for _ in range(INITIAL_SNAKE_LENGTH - 1):
        last_segment = snake[-1]
        next_segment = (last_segment[0] - 1, last_segment[1])
        snake.append(next_segment)
    return snake

def draw_food(screen, food):
    """Draw the food onto the screen.
    Do not edit this function.
    """
    if food == None:
        return
    x = food[0] * PIXELS_IN_CELL
    y = food[1] * PIXELS_IN_CELL
    pygame.draw.ellipse(screen, COLOR_FOOD, (x, y, PIXELS_IN_CELL, PIXELS_IN_CELL))

def draw_snake(screen, snake):
    """Draw the snake onto the screen.
    Do not edit this function.
    """
    color = COLOR_SNAKE_HEAD
    for segment in snake:
        x = segment[0] * PIXELS_IN_CELL
        y = segment[1] * PIXELS_IN_CELL
        pygame.draw.ellipse(screen, color, (x, y, PIXELS_IN_CELL, PIXELS_IN_CELL))
        color = COLOR_SNAKE

def draw_game_over(screen, game_over_text):
    """Draw game_over_text in the middle of the screen.
    Do not edit this function.
    """
    font_size = 50
    sys_font = pygame.font.Font(None, font_size)
    text_surface = sys_font.render(game_over_text, True, COLOR_GAME_OVER_TEXT)
    x = GRID_WIDTH_PIXELS // 2 - text_surface.get_width() // 2
    y = GRID_HEIGHT_PIXELS // 2 - text_surface.get_height() // 2
    # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
    screen.blit(text_surface, (x, y))

def draw_screen(screen, snake, food, game_over):
    """Draw the snake, food and maybe the game over message to the screen.
    Do not edit this function.
    """
    # Fill the screen with the background color.
    # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.fill
    screen.fill(COLOR_BACKGROUND)

    # Draw the snake, food, and optionally the game over message to the screen.
    draw_snake(screen, snake)
    draw_food(screen, food)
    if game_over:
        score = get_score(snake)
        game_over_text = get_game_over_text(score)
        draw_game_over(screen, game_over_text)

    # Call flip after we're done drawing this frame. This updates the entire screen.
    # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
    pygame.display.flip()

def process_events(direction, game_over):
    """Returns the new direction and whether the game should reset after processing
    all mouse and keyboard input events.
    Do not edit this function.
    """
    should_reset_game = False
    for event in pygame.event.get():
        # Quit the program when the user presses the x in the corner of the window.
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        # Process events when the user presses a key on the keyboard.
        # https://www.pygame.org/docs/ref/key.html
        elif event.type == pygame.KEYDOWN:
            # Update the snake's direction based on which key the user pressed.
            direction = get_direction(direction, event.key)
            if game_over and event.key == pygame.K_SPACE:
                # Reset all game state if the space bar is pressed after the game is over.
                should_reset_game = True
    return (direction, should_reset_game)

def start_game():
    """Starts the snake game. 
    Do not edit this function.
    """

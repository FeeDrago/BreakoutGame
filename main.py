import pygame
from constants import *

# Initialization
pygame.font.init()
pygame.mixer.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
# SOUNDS
LOST_SOUND = pygame.mixer.Sound(r'./Sounds/lost.mp3')
PADDLE_SOUND = pygame.mixer.Sound(r'./Sounds/paddle.mp3')
WALL_SOUND = pygame.mixer.Sound(r'./Sounds/wall.mp3')
BRICK_SOUND = pygame.mixer.Sound(r'./Sounds/brick.mp3')
# FONTS
FONT = pygame.font.SysFont('comicsans', 100)
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 25)

FIRST_TIME_ROOF_COLLISION = True
ORANGE_HIT = False
RED_HIT = False
GAME_FINISHED = pygame.USEREVENT + 1

def create_blocks() ->list:
    blocks = [[] for row in range(NUM_OF_ROWS)]
    for row_index, row in enumerate(blocks):
        for i in range(NUM_OF_BLOCKS_PER_ROW):
            row.append(pygame.Rect(i*BLOCK_WIDTH + (i+1) * VERTICAL_BORDER, TOP_SPACE + (row_index * (BLOCK_HEIGHT + HORIZONTAL_BORDER)),  BLOCK_WIDTH, BLOCK_HEIGHT))
    return blocks

def handle_paddle_movement(keys_pressed, paddle):
    if keys_pressed[pygame.K_LEFT] and paddle.left - PADDLE_VEL > 0: # Go Left
        paddle.x -= PADDLE_VEL
    elif keys_pressed[pygame.K_RIGHT] and paddle.left + paddle.width + PADDLE_VEL < WIDTH: # Go Right
        paddle.x += PADDLE_VEL
    

def handle_ball_movement(ball:pygame.Rect, paddle:pygame.Rect, blocks:list, points:int, lifes:int):
    global BALL_VEL, FIRST_TIME_ROOF_COLLISION, ORANGE_HIT, RED_HIT, test

    # Move Ball
    ball.x -= BALL_VEL[0]
    ball.y -= BALL_VEL[1]

    # Wall Collision
    if ball.left <= 0:
        ball.left = 0
        BALL_VEL[0] *= -1
        WALL_SOUND.play()

    elif ball.right >= WIDTH:
        ball.right = WIDTH
        BALL_VEL[0] *= -1
        WALL_SOUND.play()
    
    # Roof Collision
    if ball.top <= 0:
        ball.top = 0
        BALL_VEL[1] *= -1
        WALL_SOUND.play()
        if FIRST_TIME_ROOF_COLLISION:
            FIRST_TIME_ROOF_COLLISION = False
            paddle.width = paddle.width // 2

    # Paddle Collision
    if ball.colliderect(paddle):
        # Check if the bottom of the ball is close to the top of the paddle
        if ball.bottom >= paddle.top - 5 and ball.bottom <= paddle.top + 5:
            # Check if the center of the ball is within the horizontal boundaries of the paddle
            if paddle.left <= ball.centerx <= paddle.right:
                BALL_VEL[1] *= -1  # Reverse the vertical velocity
                PADDLE_SOUND.play()

                # Adjust the horizontal velocity based on where it hits the paddle
                ball_center = ball.centerx
                paddle_center = paddle.centerx
                offset = ball_center - paddle_center  # Calculate the offset from the center of the paddle
                max_offset = paddle.width / 2  # Maximum offset from the center of the paddle

                # Calculate the proportion of the maximum offset
                offset_factor = offset / max_offset

                # Adjust the horizontal velocity based on the offset factor
                if offset_factor < -0.5:
                    BALL_VEL[0] = -abs(BALL_VEL[0])  # Move to the left
                elif offset_factor > 0.5:
                    BALL_VEL[0] = abs(BALL_VEL[0])  # Move to the right


    

    # Block Collision
    for row_index, row in enumerate(blocks):
        for block in row:
            if block.colliderect(ball):
                points += COLOR_POINTS[row_index]
                if COLORS[row_index] == ORANGE and not ORANGE_HIT:
                    increase_ball_speed()
                    ORANGE_HIT = True
                elif COLORS[row_index] == RED and not RED_HIT:
                    increase_ball_speed()
                    RED_HIT = True
                BALL_VEL[1] *= -1
                row.remove(block)
                BRICK_SOUND.play()
                break


    # Check if all bricks are broken
    if not any(any(block for block in row) for row in blocks):
        pygame.event.post(pygame.event.Event(GAME_FINISHED))
        return points, lifes

    # Check for lost ball
    # if ball.y + BALL_RAD > HEIGHT - PADY - PADDLE_HEIGHT and not ball.colliderect(paddle):
    if ball.y + BALL_RAD > HEIGHT:
        lifes -= 1
        if lifes > 0:
            # Reset ball and paddle
            ball.x, ball.y = (WIDTH - BALL_RAD)//2, HEIGHT - 2*PADY - PADDLE_HEIGHT - BALL_RAD
            BALL_VEL = [abs(BALL_VEL[0]), abs(BALL_VEL[1])]
            paddle.x, paddle.y = (WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - PADY
        else:
            BALL_VEL = [0, 0]  # Stop the ball if no lives left

    
    return points, lifes
            
def increase_ball_speed():
    global BALL_VEL
    BALL_VEL[0] += SPEED_INCR if BALL_VEL[0] > 0 else -SPEED_INCR
    BALL_VEL[1] += SPEED_INCR if BALL_VEL[1] > 0 else -SPEED_INCR
    

def draw_window(blocks, points,lifes,  paddle, ball):

    # re-fill the window with black to remove ball trail
    WIN.fill(BLACK)

    # Draw points and lifes
    lifes_text = FONT.render(f'Lifes:{lifes}', 1 ,WHITE)
    points_text = FONT.render(f'Points:{points:03}', 1, WHITE)
    WIN.blit(lifes_text,(PADX, PADY))
    WIN.blit(points_text,(WIDTH - points_text.get_width() - PADX, PADY))

    # Draw Blocks
    for row_index, row in enumerate(blocks):
        for block in row:
            pygame.draw.rect(WIN, COLORS[row_index], block)
        
    # Draw Paddle
    pygame.draw.rect(WIN, PADDLE_COLOR, paddle)

    # Draw Ball
    pygame.draw.circle(WIN,color=WHITE, center=(int(ball.x + ball.width / 2), int(ball.y + ball.height / 2)), radius=BALL_RAD)

    pygame.display.update()

def main():
    global BALL_VEL, VEL_X, VEL_Y
    BALL_VEL = [VEL_X, VEL_Y]
    points = 0
    lifes = STARTING_LIFES
    paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - PADY, PADDLE_WIDTH, PADDLE_HEIGHT)
    blocks = create_blocks()
    ball = pygame.Rect((WIDTH - BALL_RAD)//2, HEIGHT - 2*PADY - PADDLE_HEIGHT - BALL_RAD, BALL_RAD, BALL_RAD)
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == GAME_FINISHED:
                lifes, points, running, blocks = game_over(paddle, ball, blocks, points, lifes, False, running)
        
        keys_pressed = pygame.key.get_pressed()
        handle_paddle_movement(keys_pressed, paddle)
        points, lifes = handle_ball_movement(ball, paddle, blocks, points, lifes)


        draw_window(blocks, points,lifes,  paddle, ball)

        # Check if player lost
        if lifes == 0:
            lifes, points, running, blocks = game_over(paddle, ball, blocks, points, lifes, True, running)
            

                
            

    pygame.quit()

def game_over(paddle, ball, blocks, points, lifes, lost, running):
    if lost:
        LOST_SOUND.play()
    game_over_text = GAME_OVER_FONT.render(f'You {"Lost" if lost else "Won"}! Press ESC to exit or any other key to play again.', 1, WHITE)
    WIN.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
    pygame.display.update()

    # Wait for user input to either exit or restart the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return lifes, points, running, blocks
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return lifes, points, running, blocks
                else:
                    # Reset the game and return new lifes and points
                    lifes, points, blocks = reset_game(paddle, ball, blocks, points, lifes)
                    return lifes,points, running, blocks



def reset_game(paddle, ball, blocks, points, lifes):
    global FIRST_TIME_ROOF_COLLISION, ORANGE_HIT, RED_HIT, BALL_VEL
    points = 0
    lifes = STARTING_LIFES
    FIRST_TIME_ROOF_COLLISION = True
    ORANGE_HIT, RED_HIT = False, False
    # Reset ball and paddle positions
    ball.x, ball.y = (WIDTH - BALL_RAD) // 2, HEIGHT - 2 * PADY - PADDLE_HEIGHT - BALL_RAD
    BALL_VEL = [VEL_X, VEL_Y]
    paddle.x, paddle.y = (WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - PADY
    paddle.width = PADDLE_WIDTH
    # Reset blocks
    blocks = create_blocks()
    return lifes, points, blocks

if __name__ == '__main__':
    main()
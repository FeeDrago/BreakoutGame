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
# ORANGE_HIT = pygame.USEREVENT + 1

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
    global BALL_VEL, FIRST_TIME_ROOF_COLLISION

    # Move Ball
    ball.x -= BALL_VEL[0]
    ball.y -= BALL_VEL[1]

    # Wall Collision
    if (int(ball.x + ball.width / 2) - BALL_RAD == 0) or (int(ball.x + ball.width / 2) + BALL_RAD == WIDTH ): 
        BALL_VEL[0] *= -1
        WALL_SOUND.play()
    
    # Roof Collision
    if ball.y - BALL_RAD <= 0:
        BALL_VEL[1] *= -1
        WALL_SOUND.play()
        if FIRST_TIME_ROOF_COLLISION:
            FIRST_TIME_ROOF_COLLISION = False
            paddle.width = paddle.width // 2

    # Paddle Collision
    if ball.colliderect(paddle):
        BALL_VEL[0] *= -1
        BALL_VEL[1] *= -1
        PADDLE_SOUND.play()
    
    # Block Collision
    for row_index, row in enumerate(blocks):
        for block in row:
            if block.colliderect(ball):
                points += COLOR_POINTS[row_index]
                if COLORS[row_index] == ORANGE or COLORS[row_index] == RED:
                    print(BALL_VEL)
                    increase_ball_speed()
                    print(BALL_VEL)
                BALL_VEL[1] *= -1
                row.remove(block)
                BRICK_SOUND.play()

    # Check for lost ball
    if ball.y + BALL_RAD > HEIGHT - PADY - PADDLE_HEIGHT and not ball.colliderect(paddle):
        lifes -= 1
        # Reset ball and paddle
        ball.x, ball.y =(WIDTH - BALL_RAD)//2, HEIGHT - 2*PADY - PADDLE_HEIGHT - BALL_RAD
        paddle.x, paddle.y  = (WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - PADY
        if lifes > 0:
            BALL_VEL[0] = abs(BALL_VEL[0])
            BALL_VEL[1] = abs(BALL_VEL[1])
        else: 
            BALL_VEL = [0, 0]

    
    return points, lifes
            
def increase_ball_speed():
    global BALL_VEL
    BALL_VEL[0] += 0.5 if BALL_VEL[0] > 0 else -0.5
    BALL_VEL[1] += 0.5 if BALL_VEL[1] > 0 else -0.5
    

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


        
        keys_pressed = pygame.key.get_pressed()
        handle_paddle_movement(keys_pressed, paddle)
        points, lifes = handle_ball_movement(ball, paddle, blocks, points, lifes)


        draw_window(blocks, points,lifes,  paddle, ball)

        # TODO: Check if player lost.
        if lifes == 0:
            LOST_SOUND.play()
            game_over_text = GAME_OVER_FONT.render('You Lost! Press ESC to exit or any other key to play again.', 1, WHITE)
            WIN.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
            pygame.display.update()

            # Wait for user input to either exit or restart the game
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            waiting_for_input = False
                        else:
                            # Reset game state
                            points = 0
                            lifes = STARTING_LIFES
                            # Reset ball and paddle positions
                            ball.x, ball.y = (WIDTH - BALL_RAD) // 2, HEIGHT - 2 * PADY - PADDLE_HEIGHT - BALL_RAD
                            BALL_VEL = [VEL_X, VEL_Y]
                            paddle.x, paddle.y = (WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - PADY
                            # Reset blocks
                            blocks = create_blocks()
                            waiting_for_input = False


        # TODO: Check if player broke all the bricks


    pygame.quit()


if __name__ == '__main__':
    main()
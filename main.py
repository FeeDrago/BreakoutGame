import pygame
from constants import *

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
FONT = pygame.font.SysFont('comicsans', 100)




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
    return paddle

def handle_ball_movement(ball):
    ball.x -= BALL_VEL[0]
    ball.y -= BALL_VEL[1]
    return ball



def draw_window(blocks, points, paddle, ball):

    # re-fill the window with black to remove ball trail
    WIN.fill(BLACK)


    # Draw points and lifes
    lifes_text = FONT.render(f'Lifes:{STARTING_LIFES}', 1 ,WHITE)
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
    points = 0
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
        paddle = handle_paddle_movement(keys_pressed, paddle)
        ball = handle_ball_movement(ball)


        draw_window(blocks, points, paddle, ball)

    pygame.quit()


if __name__ == '__main__':
    main()
import pygame
from constants import *
from blocks import Block
from paddle import Paddle
from ball import Ball

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
FONT = pygame.font.SysFont('comicsans', 100)

def draw_window(blocks, points, paddle, ball):

    # Draw points and lifes
    lifes_text = FONT.render(f'Lifes:{STARTING_LIFES}', 1 ,WHITE)
    points_text = FONT.render(f'Points:{points:03}', 1, WHITE)
    WIN.blit(lifes_text,(PADX, PADY))
    WIN.blit(points_text,(WIDTH - points_text.get_width() - PADX, PADY))

    # Draw Blocks
    for row in blocks:
        for block in row:
            pygame.draw.rect(WIN, block.color, block)
    
    # Draw Paddle
    pygame.draw.rect(WIN, paddle.color, paddle)

    # Draw Ball
    pygame.draw.circle(WIN,color=ball.color, center=ball.center, radius=ball.radius)




    pygame.display.update()


def create_blocks() ->list:
    blocks = [[] for row in range(NUM_OF_ROWS)]
    for row_index, row in enumerate(blocks):
        for i in range(NUM_OF_BLOCKS_PER_ROW):
            if i == 0:
                row.append(Block(i*BLOCK_WIDTH, TOP_SPACE + (row_index * (BLOCK_HEIGHT + HORIZONTAL_BORDER)),  BLOCK_WIDTH, BLOCK_HEIGHT, COLORS[row_index]))
            else:
                row.append(Block(i*(BLOCK_WIDTH + VERTICAL_BORDER), TOP_SPACE + (row_index * (BLOCK_HEIGHT + HORIZONTAL_BORDER)),  BLOCK_WIDTH, BLOCK_HEIGHT, COLORS[row_index]))
    return blocks

def handle_paddle_movement(keys_pressed, paddle):
    if keys_pressed[pygame.K_LEFT] and paddle.left - PADDLE_VEL > 0: # Go Left
        paddle.left -= PADDLE_VEL
    elif keys_pressed[pygame.K_RIGHT] and paddle.left + paddle.width + PADDLE_VEL < WIDTH: # Go Right
        paddle.left += PADDLE_VEL
    return paddle


def main():
    points = 0
    paddle = Paddle(left=(WIDTH - PADDLE_WIDTH) // 2, top=HEIGHT - PADDLE_HEIGHT - PADY,
                     width=PADDLE_WIDTH, height=PADDLE_HEIGHT, color=PADDLE_COLOR)
    blocks = create_blocks()
    ball = Ball(center=((WIDTH - BALL_RAD)//2, HEIGHT - 2*PADY - PADDLE_HEIGHT - (BALL_RAD // 2) ))
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        
        keys_pressed = pygame.key.get_pressed()
        paddle = handle_paddle_movement(keys_pressed, paddle)



        draw_window(blocks, points, paddle, ball)

    pygame.quit()


if __name__ == '__main__':
    main()
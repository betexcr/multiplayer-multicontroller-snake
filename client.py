import socket
import pickle
import pygame
import time

# Server settings
HOST = '127.0.0.1'  # Replace with server IP
PORT = 12343

# Game settings
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = 20, 20

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup display
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption("Multiplayer Snake Game")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_snake(snake, color):
    for segment in snake:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)

def draw_food(food):
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)

def main():
    # Check for controller
    pygame.joystick.init()
    has_controller = pygame.joystick.get_count() > 0
    if has_controller:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Controller connected: {joystick.get_name()}")
    else:
        print("No controller detected. Using keyboard for input.")

    # Connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print(client.recv(1024).decode())  # Welcome message

    running = True
    while running:
        try:
            # Receive game state
            data = client.recv(4096)
            game_state = pickle.loads(data)

            # Process input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            new_direction = None

            if has_controller:
                # Read controller input
                pygame.event.pump()
                x_axis = joystick.get_axis(0)  # Left stick horizontal
                y_axis = joystick.get_axis(1)  # Left stick vertical

                if y_axis < -0.5:
                    new_direction = "up"
                elif y_axis > 0.5:
                    new_direction = "down"
                elif x_axis < -0.5:
                    new_direction = "left"
                elif x_axis > 0.5:
                    new_direction = "right"
            else:
                # Read keyboard input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    new_direction = "up"
                elif keys[pygame.K_DOWN]:
                    new_direction = "down"
                elif keys[pygame.K_LEFT]:
                    new_direction = "left"
                elif keys[pygame.K_RIGHT]:
                    new_direction = "right"

            # Send direction to server
            if new_direction:
                client.send(new_direction.encode())

            # Draw game
            screen.fill(BLACK)
            draw_grid()

            for player_id, player_data in game_state["players"].items():
                color = GREEN if player_id == "player1" else BLUE
                draw_snake(player_data["snake"], color)

            draw_food(game_state["food"])

            if game_state["winner"]:
                font = pygame.font.Font(None, 36)
                message = f"Winner: {game_state['winner']}" if game_state["winner"] != "Draw" else "Draw!"
                text = font.render(message, True, WHITE)
                screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(30)
        except Exception as e:
            print(f"Error: {e}")
            running = False

    client.close()
    pygame.quit()

if __name__ == "__main__":
    main()
import socket
import threading
import pickle  # For sending game state
import time
import random

# Server settings
HOST = '0.0.0.0'
PORT = 12343

# Game settings
WIDTH, HEIGHT = 20, 20  # Grid size
TICK_RATE = 0.2  # Time between game updates (seconds)

# Directions
DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

# Game state
initial_game_state = {
    "players": {
        "player1": {"snake": [(5, 5)], "direction": "right", "alive": True},
        "player2": {"snake": [(15, 15)], "direction": "left", "alive": True},
    },
    "food": (10, 10),
    "winner": None,
}

game_state = dict(initial_game_state)
restart_votes = {"player1": False, "player2": False}

# Lock for thread safety
lock = threading.Lock()

def reset_game():
    """Reset the game state."""
    global game_state, restart_votes
    game_state = dict(initial_game_state)
    restart_votes = {"player1": False, "player2": False}

def handle_player(conn, player_id):
    """Handle communication with a player."""
    conn.send(f"Welcome {player_id}!\n".encode())
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if data == "restart":
                with lock:
                    restart_votes[player_id] = True
                    if all(restart_votes.values()):
                        reset_game()
            elif data in DIRECTIONS:
                with lock:
                    if game_state["players"][player_id]["alive"]:
                        game_state["players"][player_id]["direction"] = data
        except:
            break
    conn.close()

def game_logic():
    """Main game loop."""
    while True:
        time.sleep(TICK_RATE)
        with lock:
            if game_state["winner"] is not None:
                continue

            for player_id, player_data in game_state["players"].items():
                if not player_data["alive"]:
                    continue

                # Move snake
                direction = DIRECTIONS[player_data["direction"]]
                head = player_data["snake"][-1]
                new_head = (head[0] + direction[0], head[1] + direction[1])

                # Check for collisions
                if (
                    new_head[0] < 0 or new_head[0] >= WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT or
                    new_head in player_data["snake"]
                ):
                    player_data["alive"] = False
                    continue

                for other_player_id, other_player_data in game_state["players"].items():
                    if player_id != other_player_id and new_head in other_player_data["snake"]:
                        player_data["alive"] = False
                        continue

                # Update snake
                player_data["snake"].append(new_head)
                if new_head == game_state["food"]:
                    game_state["food"] = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
                else:
                    player_data["snake"].pop(0)

            # Check for winner
            alive_players = [p for p in game_state["players"].values() if p["alive"]]
            if len(alive_players) == 1:
                game_state["winner"] = next(
                    player_id for player_id, p in game_state["players"].items() if p["alive"]
                )
            elif len(alive_players) == 0:
                game_state["winner"] = "Draw"

def broadcast_game_state(connections):
    """Send the game state to all clients."""
    while True:
        time.sleep(TICK_RATE)
        with lock:
            state_data = pickle.dumps(game_state)
        for conn in connections:
            try:
                conn.send(state_data)
            except:
                connections.remove(conn)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Server started on {HOST}:{PORT}")

    connections = []
    players = ["player1", "player2"]
    threads = []

    # Accept players
    for i in range(2):
        conn, addr = server.accept()
        print(f"{players[i]} connected from {addr}")
        connections.append(conn)
        t = threading.Thread(target=handle_player, args=(conn, players[i]))
        threads.append(t)
        t.start()

    print("Both players connected. Starting game...")
    threading.Thread(target=game_logic).start()
    threading.Thread(target=broadcast_game_state, args=(connections,)).start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
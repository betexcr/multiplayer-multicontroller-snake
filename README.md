# 🐍 Multiplayer Multicontroller Snake

**Multiplayer Multicontroller Snake** is an online multiplayer version of the classic Snake game, built with Python. It supports unlimited players and multiple input methods, including keyboard and game controllers. This project includes both server and client components for a smooth real-time gameplay experience.

## 🎮 Features

- **Unlimited players** – anyone can join!
- **Supports multiple controllers** – keyboard or any gamepad input.
- **Real-time multiplayer** – server-client architecture keeps all players in sync.
- **Hot-seat capable** – play locally or over a network.

## 🛠️ Tech Stack

- **Language**: Python
- **Networking**: `socket` (standard Python library)
- **Graphics & Input**: `pygame` for rendering and input
- **Architecture**: Client-server model

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/betexcr/multiplayer-multicontroller-snake.git
cd multiplayer-multicontroller-snake
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Start the Server
```bash
python server.py
```
### 4. Start the Clients

Run this on each player’s machine (or multiple times locally):
```bash
python client.py
```

Make sure all clients are on the same network or can connect to the server’s IP address.

## 🏁 Gameplay

- Players move snakes to collect apples and grow.
- Colliding with another snake or a wall ends the round.
- The player with the highest score wins.

## 🤝 Contributions

Pull requests are welcome! If you have suggestions or improvements, feel free to fork the repo and submit a PR.

## 📄 License

Licensed under the MIT License.

---

Enjoy the chaos! 🐍🕹️

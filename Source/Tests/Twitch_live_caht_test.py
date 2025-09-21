import socket
import os
from dotenv import load_dotenv

load_dotenv()

TWITCH_SERVER = "irc.chat.twitch.tv"
TWITCH_PORT = 6667
TWITCH_NICK = os.getenv("TWITCH_NICK")
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")


def connect_to_twitch(channel):
    sock = socket.socket()
    sock.connect((TWITCH_SERVER, TWITCH_PORT))
    sock.send(f"PASS {TWITCH_TOKEN}\r\n".encode("utf-8"))
    sock.send(f"NICK {TWITCH_NICK}\r\n".encode("utf-8"))
    sock.send(f"JOIN #{channel}\r\n".encode("utf-8"))
    return sock


def print_twitch_chat(channel):
    sock = connect_to_twitch(channel)
    print(f"✅ Connected to Twitch channel: {channel}")

    while True:
        response = sock.recv(2048).decode("utf-8")

        if response.startswith("PING"):
            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            continue

        parts = response.split(":", 2)
        if len(parts) < 3:
            continue

        username = parts[1].split("!")[0]
        message = parts[2].strip()
        print(f"{username}: {message}")


if __name__ == "__main__":
    # Replace with any live Twitch channel name
    print_twitch_chat("shroud")

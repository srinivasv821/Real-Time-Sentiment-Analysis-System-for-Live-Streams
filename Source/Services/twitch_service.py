import socket
import os
from dotenv import load_dotenv

load_dotenv()

TWITCH_SERVER = "irc.chat.twitch.tv"
TWITCH_PORT = 6667
TWITCH_NICK = os.getenv("TWITCH_NICK")
TWITCH_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")


def connect_to_twitch(channel):
    sock = socket.socket()
    sock.connect((TWITCH_SERVER, TWITCH_PORT))
    sock.send(f"PASS {TWITCH_TOKEN}\r\n".encode("utf-8"))
    sock.send(f"NICK {TWITCH_NICK}\r\n".encode("utf-8"))
    sock.send(f"JOIN #{channel}\r\n".encode("utf-8"))
    return sock


def fetch_twitch_chat(channel, limit=10):
    """Fetch a batch of chat messages from Twitch"""
    sock = connect_to_twitch(channel)
    messages = []
    while len(messages) < limit:
        response = sock.recv(2048).decode("utf-8")

        if response.startswith("PING"):
            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            continue

        parts = response.split(":", 2)
        if len(parts) < 3:
            continue

        username = parts[1].split("!")[0]
        message = parts[2].strip()
        messages.append({"author": username, "message": message})

    sock.close()
    print(messages)
    return messages

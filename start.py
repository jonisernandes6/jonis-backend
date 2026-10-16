import subprocess
import sys
import os
import signal
import time

def run_process(cmd, name):
    print(f"Starting {name}...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

# Iniciar el servidor web
web_process = run_process([sys.executable, "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "app:app"], "Web Server")

# Iniciar el bot
bot_process = run_process([sys.executable, "bot.py"], "Telegram Bot")

try:
    # Esperar a que ambos terminen o a que uno falle
    web_process.wait()
    bot_process.wait()
except KeyboardInterrupt:
    print("\nShutting down services...")
    web_process.terminate()
    bot_process.terminate()
    web_process.wait()
    bot_process.wait()
    print("Services stopped.")

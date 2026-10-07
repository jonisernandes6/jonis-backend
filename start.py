import subprocess

web = subprocess.Popen(["gunicorn", "app:app"])
bot = subprocess.Popen(["python", "bot.py"])

web.wait()
bot.wait()

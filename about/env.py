import os
BOT_TOKEN = "7877006012:AAG0WsYqU6XnmAZ3QYdu-WdmIE3sB6qSDBM"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
file_path = os.path.join(BASE_DIR, "Admins.txt")  # Load the file

try:
    with open(file_path, "r", encoding="utf-8") as f:  # Explicitly set encoding to avoid issues
        ADMINS = [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]  # Read & parse as list of integers
    print("ADMINS List:", ADMINS)
except FileNotFoundError:
    print("Admins.txt not found! Check the file path.")
    ADMINS = []
except ValueError as e:
    print("Admins.txt contains non-numeric values!", e)
    ADMINS = []
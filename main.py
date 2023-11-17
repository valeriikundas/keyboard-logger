from pynput import keyboard
import time
import os

# Set of keys that will be considered as special keys
special_keys = set(['ctrl', 'alt', 'opt', 'shift'])

# Log file to store the shortcuts
log_file = 'shortcut_log.txt'

# Time window for detecting consecutive key presses
time_window = 0.3  # in seconds

# Variables to store the last key press information
last_key = None
last_key_time = None

# Function to write the shortcut to the log file and stdout
def log_shortcut(shortcut):
    with open(log_file, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {shortcut}\n")
    print(shortcut)

# Function to handle key press events
def on_press(key):
    global last_key, last_key_time

    try:
        # Get the name of the pressed key
        key_name = key.char
    except AttributeError:
        # Handle special keys
        key_name = str(key).split('.')[-1]

    # Check if the key is a special key
    if key_name.lower() in special_keys:
        # Check for consecutive key presses within the time window
        current_time = time.time()
        if last_key_time is not None and current_time - last_key_time < time_window:
            # Log the shortcut
            log_shortcut(f"{last_key} + {key_name}")
            last_key_time = None  # Reset the timestamp after logging the shortcut
        else:
            # Update the timestamp for the first key press
            last_key_time = current_time
            last_key = key_name

# Function to handle key release events
def on_release(key):
    pass

# Ensure the log file exists or create it
if not os.path.isfile(log_file):
    with open(log_file, 'w'):
        pass

# Set up the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listening for shortcuts. Press Ctrl+C to stop.")
    listener.join()

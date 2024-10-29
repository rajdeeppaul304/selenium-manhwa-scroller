import json
import os
from pynput import mouse

# Path to the existing JSON file
filename = 'data.json'

# Load existing data from the JSON file
if os.path.exists(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
else:
    data = {}

# List to store the coordinates
coordinates = []

# Callback function to capture mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        coordinates.append((x, y))
        print(f"Clicked at ({x}, {y})")
        
        # Stop listening after 4 clicks
        if len(coordinates) >= 4:
            return False

# Start listening for mouse clicks
with mouse.Listener(on_click=on_click) as listener:
    print("Click on the corners (top-left, top-right, bottom-left, bottom-right).")
    listener.join()

# Calculate coordinates
top_left, top_right, bottom_left, bottom_right = coordinates
x = top_left[0]
y = top_left[1]
width = top_right[0] - top_left[0]
height = bottom_left[1] - top_left[1]

# Update the coordinates_for_screenshot key
data['coordinates_for_screenshot'] = {
    "x": x,
    "y": y,
    "width": width,
    "height": height
}

# Save updated data back to the JSON file
with open(filename, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Coordinates have been updated in '{filename}'.")

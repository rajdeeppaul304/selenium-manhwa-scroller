from selenium import webdriver
from PIL import Image
import pytesseract
import time
import json
import os

scroll_distance = 0
continue_scrolling = True
driver = None

filename = 'data.json'

if os.path.exists(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        coordinates = data.get('coordinates_for_screenshot', {})
        
        x = coordinates.get('x', 0)
        y = coordinates.get('y', 0)
        width = coordinates.get('width', 0)
        height = coordinates.get('height', 0)

        character_per_minute = data.get('character_per_minute', 1200)
else:
    print("data file not found.")
    exit()

def get_screenshot_of_area(driver, x, y, width, height):
    screenshot = driver.get_screenshot_as_png()
    with open('full_screenshot.png', 'wb') as f:
        f.write(screenshot)
    
    image = Image.open('full_screenshot.png')
    cropped_image = image.crop((x, y, x + width, y + height))
    cropped_image.save('cropped_screenshot.png')

    return 'cropped_screenshot.png'  # Return the path of the cropped image

def calculate_reading_time(image_path):
    # Use Tesseract to perform OCR on the cropped image
    text = pytesseract.image_to_string(Image.open(image_path))
    print(text)
    # Calculate reading time based on character count
    char_count = len(text)
    print(character_per_minute)
    time_per_character = 60 / character_per_minute  # Assume 200 characters per minute
    total_time = int(char_count * time_per_character * 1000)  # Convert to milliseconds

    if total_time == 0:
        total_time = 200  # Ensure there's at least 1 ms to wait
    
    return total_time

# Load coordinates from the JSON file







# Start the Selenium WebDriver
driver = webdriver.Chrome()
driver.get('https://google.com/')
# driver.fullscreen_window()

# Allow time for the page to load
time.sleep(2)

# try:
#     element = driver.find_element("css selector", ".w-12.h-12.overflow-y-hidden.flex.items-center.hover\\:bg-gray-200.dark\\:hover\\:bg-gray-600.cursor-pointer")
#     element.click()
# except Exception as e:
#     print(f"An error occurred: {e}")
# time.sleep(2)


def create_scroll_checkbox(driver):
    # Check if the checkbox already exists
    checkbox_exists = driver.execute_script("return document.getElementById('scrollCheckbox') !== null;")
    
    if not checkbox_exists:
        driver.execute_script("""
            var label = document.createElement('label');
            label.innerHTML = 'Scrolling';
            label.style.position = 'fixed';
            label.style.left = '10px';
            label.style.top = '10px';
            label.style.zIndex = '1000';
            label.style.fontSize = '20px';  // Make label text bigger
            document.body.appendChild(label);
            
            var checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = 'scrollCheckbox';
            checkbox.style.position = 'fixed';
            checkbox.style.left = '120px';  // Position checkbox next to the label
            checkbox.style.top = '10px';
            checkbox.style.zIndex = '10000000';
            checkbox.style.transform = 'scale(1.5)';  // Make checkbox bigger
            checkbox.checked = false;  // Start with scrolling disabled
            document.body.appendChild(checkbox);
        """)

def start_scrolling(driver, x, y, width, height):
    scroll_distance = 0
    last_scroll_position = driver.execute_script("return window.scrollY;")  # Initialize last position

    while True:
        create_scroll_checkbox(driver)
        # Check if scrolling is enabled
        scrolling_enabled = driver.execute_script("return document.getElementById('scrollCheckbox').checked;")
        
        if not scrolling_enabled:
            print("Scrolling paused by user.")
            last_scroll_position = driver.execute_script("return window.scrollY;")
            time.sleep(1)  # Pause for a bit before checking again
            continue

        # Take a screenshot of the specified area
        image_path = get_screenshot_of_area(driver, x, y, width, height)

        # Calculate the reading time from the cropped screenshot
        reading_time = calculate_reading_time(image_path)
        print(f"Reading time (ms): {reading_time}")

        # Wait for the calculated reading time
        time.sleep(reading_time / 1000.0)  # Convert ms to seconds

        # Get the current scroll position
        current_scroll_position = driver.execute_script("return window.scrollY;")

        if current_scroll_position != last_scroll_position:
            print("User has scrolled manually. Stopping automated scrolling.")
            driver.execute_script("document.getElementById('scrollCheckbox').checked = false;")
        
        # Scroll down
        scroll_distance += (driver.execute_script("return window.innerHeight;") - 100)
        driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_distance)
        last_scroll_position = driver.execute_script("return window.scrollY;")

        # Check if we reached the bottom of the page
        if (scroll_distance + driver.execute_script("return window.innerHeight;")) >= driver.execute_script("return document.body.scrollHeight;"):
            print("Reached the bottom of the page.")
            break




scroll_distance = 0
last_scroll_position = driver.execute_script("return window.scrollY;")  # Initialize last position

create_scroll_checkbox(driver)

start_scrolling(driver, x, y, width, height)



# Close the WebDriver
# driver.quit()
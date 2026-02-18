import sys
import webbrowser
import pyautogui
import time

import numpy as np
import cv2

def find_with_opencv(template_path, threshold=0.85):
    # Take a screenshot and convert it to OpenCV format (grayscale)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Load the template image and convert to grayscale too
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"Error: {template_path} not found or failed to load.")
        return None

    # If template has alpha channel, drop it
    if len(template.shape) == 3 and template.shape[-1] == 4:
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    elif len(template.shape) == 3:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Match the template on the screen
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Debug output
    print(f"[DEBUG] Match confidence: {max_val:.3f}")

    # If match is strong enough, return the center position
    if max_val >= threshold:
        template_h, template_w = template.shape[:2]
        center_x = max_loc[0] + template_w // 2
        center_y = max_loc[1] + template_h // 2
        print(f"Found {template_path} at ({center_x}, {center_y})")
        return (center_x, center_y)

    return None


def locate_and_click(image_path, retries=3, threshold=0.85):
    for attempt in range(retries):
        coords = find_with_opencv(image_path, threshold)
        if coords:
            time.sleep(1)
            pyautogui.click(coords)
            return True
        else:
            print(f"{image_path} not found, retrying ({attempt + 1}/{retries})...")
            time.sleep(2)
    print(f"{image_path} not found after {retries} attempts.")
    return False


if len(sys.argv) < 2:
    print("Usage: python AskFreeGPT.py <query>")
    sys.exit(1)

query = sys.argv[1]

webbrowser.open("https://chatgpt.com")
time.sleep(10)  # wait for browser to load

pyautogui.write(query)
time.sleep(2)

# Try to find and click the image "1.png"
if not locate_and_click("1.png"):
    print("ErrorNoSEND")
time.sleep(60)

if not locate_and_click("StayOFFLINE.png"):
    print("NO LOGIN POP-UP")


if not locate_and_click("Copy.png"):
    print("ErrorNoCOPY")
    if not locate_and_click("Copy2.png"):
        print("ErrorNoCOPY2")

import cv2
import numpy as np

# Simplified color dictionary for basic hues (Red, Green, Blue, etc.)
basic_color_dict = {
    (255, 0, 0): 'Red',
    (0, 255, 0): 'Green',
    (255, 140, 0): 'Blue',
    (0, 255, 255): 'Yellow',
    (0, 0, 255): 'Orange',
    (128, 0, 128): 'Purple',
    (255, 255, 0): 'Cyan',
    (255, 0, 255): 'Magenta',
    (0, 0, 0): 'Black',
    (255, 255, 255): 'White'
}

# Global variables
detection_active = True
daltonize_active = False  # New state for daltonize mode
cvd_type = 'None'  # Tracks CVD type
mouse_color_label = ""  
mouse_color_rgb = ""    
mouse_x, mouse_y = -1, -1  
image_index = 0  

# List of images
image_paths = [
    "D:\MIT FULL NOTES\MIT PROJECT\DATA SETS\Color Sets\P1 - 14-10-2024\colorful-collection-balls-with-lot-different-colors_931553-166354.jpg",
    "D:\MIT FULL NOTES\MIT PROJECT\DATA SETS\Color Sets\P1 - 14-10-2024\colorful-collection-balls-with-lot-different-colors_931553-166354.jpg",
    "D:\MIT FULL NOTES\MIT PROJECT\DATA SETS\Color Sets\P1 - 14-10-2024\colorful-collection-balls-with-lot-different-colors_931553-166354.jpg"
]

# Daltonize matrices for different color vision deficiencies (simplified)
cvd_matrices = {
    'Protanopia': np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]]),
    'Deuteranopia': np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]]),
    'Tritanopia': np.array([[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]])
}

# Function to detect objects
def detect_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_val = np.array([0, 40, 40])
    upper_val = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_val, upper_val)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Function to draw highlighted contours
def draw_highlighted_contour(frame, contours):
    highlighted = False
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            if cv2.pointPolygonTest(cnt, (mouse_x, mouse_y), False) >= 0:
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                highlighted = True
            else:
                cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)

# Daltonization function
def daltonize_image(image, cvd_type):
    if cvd_type in cvd_matrices:
        cvd_matrix = cvd_matrices[cvd_type]
        reshaped_img = image.reshape((-1, 3)).astype(np.float32) / 255.0
        transformed_img = np.dot(reshaped_img, cvd_matrix.T)
        transformed_img = np.clip(transformed_img, 0, 1) * 255
        return transformed_img.reshape(image.shape).astype(np.uint8)
    return image

# Mouse callback function to display color and RGB values on hover
def show_color(event, x, y, flags, param):
    global mouse_color_label, mouse_color_rgb, mouse_x, mouse_y
    mouse_x, mouse_y = x, y
    if event == cv2.EVENT_MOUSEMOVE:
        color = frame[y, x]
        closest_color = min(basic_color_dict.keys(), key=lambda c: np.linalg.norm(np.array(color) - np.array(c)))
        mouse_color_label = basic_color_dict[closest_color]
        mouse_color_rgb = f"RGB: ({color[2]}, {color[1]}, {color[0]})"

# Load the current image
def load_image(index):
    image = cv2.imread(image_paths[index])
    if image is None:
        print(f"Error: Unable to load image at {image_paths[index]}")
    return image

# Set mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", show_color)

# Display the image with highlighted objects
while True:
    frame = load_image(image_index)
    
    if frame is None:
        key = cv2.waitKey(1)
        continue
    
    display_frame = frame.copy()

    if daltonize_active and cvd_type != 'None':
        display_frame = daltonize_image(display_frame, cvd_type)

    if detection_active:
        contours = detect_objects(display_frame)
        draw_highlighted_contour(display_frame, contours)

    if mouse_color_label:
        cv2.putText(display_frame, f"Color: {mouse_color_label}  {mouse_color_rgb}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 241, 0), 2)

    cv2.imshow("Image", display_frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC key to exit
        break
    elif key == ord('d'):  # Toggle detection with 'd' key
        detection_active = not detection_active
    elif key == ord('n'):  # Next image with 'n' key
        image_index = (image_index + 1) % len(image_paths)
    elif key == ord('p'):  # Previous image with 'p' key
        image_index = (image_index - 1) % len(image_paths)
    elif key == ord('c'):  # Toggle Daltonize mode with 'c' key
        daltonize_active = not daltonize_active
    elif key == ord('1'):  # Apply Protanopia Daltonization
        cvd_type = 'Protanopia'
        daltonize_active = True
    elif key == ord('2'):  # Apply Deuteranopia Daltonization
        cvd_type = 'Deuteranopia'
        daltonize_active = True
    elif key == ord('3'):  # Apply Tritanopia Daltonization
        cvd_type = 'Tritanopia'
        daltonize_active = True
    elif key == ord('r'):  # Reset/Disable Daltonization
        daltonize_active = False
        cvd_type = 'None'

    if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break

# Cleanup
cv2.destroyAllWindows()
"""""
CVD mode switching:
You can switch between different CVD modes using keys:
'1' for Protanopia
'2' for Deuteranopia
'3' for Tritanopia
'r' to reset/disable Daltonize.
"""
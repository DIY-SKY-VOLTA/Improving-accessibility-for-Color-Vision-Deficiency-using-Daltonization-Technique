# Install the libraries before execution

import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from scipy.spatial import KDTree

# Predefined color dictionary with their RGB values
COLOR_LIBRARY = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Gray": (128, 128, 128),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
}

# Build KDTree for fast nearest neighbor search
color_names = list(COLOR_LIBRARY.keys())
color_values = np.array(list(COLOR_LIBRARY.values()))
color_tree = KDTree(color_values)

def daltonize(image_array, deficiency):
    """
    Apply daltonization to an image based on the specified color vision deficiency or enhancement filter.
    """
    if deficiency == 'protan':
        matrix = np.array([[0.56667, 0.43333, 0],
                           [0.55833, 0.44167, 0],
                           [0, 0.24167, 0.75833]])
    elif deficiency == 'deutan':
        matrix = np.array([[0.4251, 0.6934, -0.1147],
                           [0.3417, 0.5882, 0.0692],
                           [-0.0105, 0.0234, 0.987]])
    elif deficiency == 'tritan':
        matrix = np.array([[0.95, 0.05, 0],
                           [0, 0.83333, 0.167],
                           [0, 0.875, 0.125]])
    elif deficiency == 'monochromacy':
        matrix = np.array([[0.33, 0.33, 0.33],
                           [0.33, 0.33, 0.33],
                           [0.33, 0.33, 0.33]])
    elif deficiency == 'blue_cone':
        matrix = np.array([[0.5, 0.5, 0],
                           [0, 0.5, 0.5],
                           [0, 0, 1]])
    elif deficiency == 'enhance-r':
        matrix = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [1, 0, 0]])
    elif deficiency == 'enhance-g':
        matrix = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 1, 0]])
    else:
        raise ValueError("Invalid deficiency or enhancement type.")

    daltonized_image = np.dot(image_array[..., :3], matrix.T)
    daltonized_image = np.clip(daltonized_image, 0, 255).astype(np.uint8)
    
    return daltonized_image

def open_image():
    """Open an image file."""
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
    if file_path:
        load_and_display_image(file_path)

def load_and_display_image(image_path):
    """Load and display the selected image."""
    global original_image_array
    original_image = Image.open(image_path).convert('RGB')
    original_image_array = np.array(original_image)  # Convert to numpy array
    show_image(original_image_array)

def show_image(image_array):
    """Show the image in the Tkinter window."""
    image = Image.fromarray(image_array)
    image.thumbnail((400, 400))  # Resize for display
    img_tk = ImageTk.PhotoImage(image)

    # Clear previous image
    for widget in frame.winfo_children():
        widget.destroy()

    label = tk.Label(frame, image=img_tk)
    label.image = img_tk  # Keep a reference
    label.pack()

def apply_daltonization(deficiency):
    """Apply the selected CVD category or enhancement and display the image."""
    if original_image_array is not None:
        daltonized_image = daltonize(original_image_array, deficiency)
        show_image(daltonized_image)

def disable_daltonization():
    """Display the original image without any daltonization."""
    if original_image_array is not None:
        show_image(original_image_array)

def recognize_color(rgb_value):
    """Recognize the closest predefined color from the library."""
    _, idx = color_tree.query(rgb_value)
    return color_names[idx]

def get_average_color(image_array, x, y, region_size=5):
    """Get the average color from a small region around the mouse cursor."""
    height, width, _ = image_array.shape
    x_start = max(0, x - region_size)
    y_start = max(0, y - region_size)
    x_end = min(width, x + region_size)
    y_end = min(height, y + region_size)

    region = image_array[y_start:y_end, x_start:x_end]
    avg_color = np.mean(region, axis=(0, 1))
    return avg_color

def on_mouse_move(event):
    """Handle mouse movement and display the color under the cursor."""
    if original_image_array is not None:
        x, y = event.x, event.y
        avg_color = get_average_color(original_image_array, x, y)
        recognized_color = recognize_color(avg_color)
        color_info_label.config(text=f"RGB: {avg_color.astype(int)} | Color: {recognized_color}")

# Create the main window
root = tk.Tk()
root.title("Color Vision Deficiency Simulator")

frame = tk.Frame(root)
frame.pack()

# Add buttons for CVD categories and enhancements
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_protan = tk.Button(button_frame, text="Protanopia", command=lambda: apply_daltonization('protan'))
btn_protan.pack(side=tk.LEFT)

btn_deutan = tk.Button(button_frame, text="Deuteranopia", command=lambda: apply_daltonization('deutan'))
btn_deutan.pack(side=tk.LEFT)

btn_tritan = tk.Button(button_frame, text="Tritanopia", command=lambda: apply_daltonization('tritan'))
btn_tritan.pack(side=tk.LEFT)

btn_monochromacy = tk.Button(button_frame, text="Monochromacy", command=lambda: apply_daltonization('monochromacy'))
btn_monochromacy.pack(side=tk.LEFT)

btn_blue_cone = tk.Button(button_frame, text="Blue Cone Monochromacy", command=lambda: apply_daltonization('blue_cone'))
btn_blue_cone.pack(side=tk.LEFT)

btn_enhance_r = tk.Button(button_frame, text="Enhance Red", command=lambda: apply_daltonization('enhance-r'))
btn_enhance_r.pack(side=tk.LEFT)

btn_enhance_g = tk.Button(button_frame, text="Enhance Green", command=lambda: apply_daltonization('enhance-g'))
btn_enhance_g.pack(side=tk.LEFT)

btn_disable = tk.Button(button_frame, text="Disable", command=disable_daltonization)
btn_disable.pack(side=tk.LEFT)

btn_load_image = tk.Button(root, text="Load Image", command=open_image)
btn_load_image.pack(pady=20)

# Label to show the recognized color
color_info_label = tk.Label(root, text="Hover over the image to see color information.")
color_info_label.pack(pady=10)

original_image_array = None

# Bind the mouse motion event to display color under cursor
root.bind('<Motion>', on_mouse_move)

# Start the Tkinter main loop
root.mainloop()


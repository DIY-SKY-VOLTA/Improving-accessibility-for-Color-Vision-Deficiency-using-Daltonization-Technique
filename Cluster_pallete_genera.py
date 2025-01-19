#########  ***** EXTRACTED CLUSTER COLOR PALLETE GENERATOR USING IMPROVED OCTREE QUONTIZATION METHOD  ******  ########## 

#  Extracted cluster palettes are a visually organized collection of key colors from an image,
#  created through automated processes that identify and group similar colors effectively.

from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import random
import tkinter as tk
from tkinter import filedialog

def rgb_to_hsv(color):
    """Convert an RGB color to HSV."""
    color = np.array(color)  # Convert list to NumPy array
    r, g, b = color / 255.0  # Normalize RGB values to [0, 1]
    return colorsys.rgb_to_hsv(r, g, b)  # Returns (hue, saturation, value)

def hsv_to_rgb(color):
    """Convert an HSV color to RGB."""
    h, s, v = color
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return [int(r * 255), int(g * 255), int(b * 255)]  # Convert back to [0, 255]

def generate_random_color():
    """Generate a random RGB color."""
    return [random.randint(0, 255) for _ in range(3)]

def extract_color_palettes(image_path, n_colors, grid_rows, grid_cols, max_iterations=10):
    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")  # Ensure the image is in RGB format
    image = image.resize((300, 300))  # Resize for efficiency
    image_np = np.array(image).reshape((-1, 3))  # Reshape to (pixels, RGB)
    
    # Prepare to collect all colors
    all_colors = []
    
    for _ in range(max_iterations):
        if len(all_colors) >= n_colors:
            break  # Stop if we've gathered enough colors
        
        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=min(n_colors - len(all_colors), len(image_np)), random_state=42).fit(image_np)
        colors = kmeans.cluster_centers_.astype(int)
        all_colors.extend(colors)

        # Remove pixels close to the extracted colors
        distances = np.linalg.norm(image_np[:, None] - colors[None, :], axis=2)
        min_distances = np.min(distances, axis=1)
        image_np = image_np[min_distances > 30]  # Keep only pixels far from extracted colors

        if len(image_np) < 1:  # Break if no pixels remain
            break

    # Ensure at least n_colors by repeating or padding
    while len(all_colors) < n_colors:
        all_colors.append([255, 255, 255])  # Add white as padding if necessary
    all_colors = all_colors[:n_colors]  # Trim excess colors

    # Remove white colors (close to [255, 255, 255]) and replace with random colors
    all_colors = [color for color in all_colors if not (color[0] > 240 and color[1] > 240 and color[2] > 240)]
    
    while len(all_colors) < n_colors:
        all_colors.append(generate_random_color())  # Replace with a new random color

    # Sort colors based on their hue and saturation in HSV color space for better visual grouping
    all_colors_hsv = [rgb_to_hsv(color) for color in all_colors]
    
    # Sort primarily by hue and secondarily by saturation for better grouping of similar colors
    sorted_colors_hsv = sorted(all_colors_hsv, key=lambda x: (x[0], x[1]))  
    sorted_rgb_colors = [hsv_to_rgb(color) for color in sorted_colors_hsv]

    # Reshape sorted colors into a grid for vertical grouping (columns represent similar hues)
    grouped_rgb_colors = np.array(sorted_rgb_colors).reshape(grid_cols, grid_rows, -1).transpose(1, 0, 2)

    # Create the grid for the palette
    fig, ax = plt.subplots(grid_rows, grid_cols, figsize=(14, 7))
    fig.suptitle("Extracted Color Palettes", fontsize=16)

    for i in range(grid_rows):
        for j in range(grid_cols):
            ax[i][j].axis("off")
            color = grouped_rgb_colors[i][j] / 255.0  # Normalize RGB for display
            ax[i][j].imshow([[color]])  # Pass normalized RGB as a 2D array

    plt.tight_layout()
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Prompt user to select an image file
    image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    
    if image_path: 
        n_colors = 98   # Total number of colors needed (7 rows x 14 columns)
        grid_rows = 7   # Number of rows in the palette grid
        grid_cols = 14   # Number of columns in the palette grid
        
        extract_color_palettes(image_path, n_colors, grid_rows, grid_cols)

if __name__ == "__main__":
    main()


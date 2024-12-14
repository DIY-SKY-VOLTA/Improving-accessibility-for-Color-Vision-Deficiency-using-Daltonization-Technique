
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def daltonize(image_array, deficiency):
    """
    Apply daltonization to an image based on the specified color vision deficiency.
    
    Parameters:
        image_array (numpy array): The RGB image array.
        deficiency (str): Type of color vision deficiency ('protan', 'deutan', 'tritan', 'monochromacy', 'enhance_r', 'enhance_g').
    
    Returns:
        numpy array: The daltonized image array.
    """
    # Define transformation matrices for different deficiencies
    if deficiency == 'protan':
        matrix = np.array([[0.56667, 0.43333, 0.00000],
                           [0.55833, 0.44167, 0.00000],
                           [0.00000, 0.24167, 0.75833]])
    elif deficiency == 'deutan':
        matrix = np.array([[0.4251, 0.6934, -0.1147],
                           [0.3417, 0.5882, 0.0692],
                           [-0.0105, 0.0234, 0.9870]])
    elif deficiency == 'tritan':
        matrix = np.array([[0.95000, 0.05000, 0.00000],
                           [0.00000, 0.83333, 0.16700],
                           [0.00000, 0.87500, 0.12500]])
    elif deficiency == 'monochromacy':
        matrix = np.array([[0.33, 0.33, 0.33],
                           [0.33, 0.33, 0.33],
                           [0.33, 0.33, 0.33]])
    elif deficiency == 'enhance_r':
        matrix = np.array([[1.00, 0.00, 0.00],
                           [0.00, 1.00, 0.00],
                           [1.00, 0.00, 0.00]])
    elif deficiency == 'enhance_g':
        matrix = np.array([[1.00, 0.00, 0.00],
                           [0.00, 1.00, 0.00],
                           [0.00, 1.00, 0.00]])
    else:
        raise ValueError("Invalid deficiency type.")

    # Apply the transformation
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
    global original_image_array, processed_image_array
    original_image = Image.open(image_path).convert('RGB')
    original_image_array = np.array(original_image)  # Convert to numpy array
    processed_image_array = None  # Reset processed image
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
    """Apply the selected CVD category and display the image."""
    global processed_image_array
    if original_image_array is not None:
        processed_image_array = daltonize(original_image_array, deficiency)
        show_image(processed_image_array)

def save_image():
    """Save the processed (daltonized) image."""
    if processed_image_array is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                 filetypes=[("PNG files", "*.png"), 
                                                            ("JPEG files", "*.jpg"), 
                                                            ("All files", "*.*")])
        if save_path:
            save_image = Image.fromarray(processed_image_array)
            save_image.save(save_path)
            messagebox.showinfo("Save Image", f"Image saved successfully as {save_path}")
            
            # Ask if the user wants to open the folder
            open_folder = messagebox.askyesno("Open Folder", "Do you want to open the folder containing the saved image?")
            if open_folder:
                folder_path = os.path.dirname(save_path)
                os.startfile(folder_path)  # Opens the folder in the file explorer
    else:
        messagebox.showwarning("Save Image", "No daltonized image to save. Apply a filter first!")

# Create the main window
root = tk.Tk()
root.title("Color Vision Deficiency Simulator")

frame = tk.Frame(root)
frame.pack()

# Add buttons for CVD categories
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

btn_enhance_r = tk.Button(button_frame, text="Enhance Red", command=lambda: apply_daltonization('enhance_r'))
btn_enhance_r.pack(side=tk.LEFT)

btn_enhance_g = tk.Button(button_frame, text="Enhance Green", command=lambda: apply_daltonization('enhance_g'))
btn_enhance_g.pack(side=tk.LEFT)

btn_load_image = tk.Button(root, text="Load Image", command=open_image)
btn_load_image.pack(pady=20)

btn_save_image = tk.Button(root, text="Save Image", command=save_image)
btn_save_image.pack(pady=10)

original_image_array = None
processed_image_array = None  # Store the processed image

# Start the Tkinter main loop
root.mainloop()

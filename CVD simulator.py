import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import ipywidgets as widgets
from IPython.display import display

# Define CVD transformation matrices
cvd_matrices = {
    'Protanopia': np.array([[0.56667, 0.43333, 0.0],
                            [0.55833, 0.44167, 0.0],
                            [0.0, 0.24167, 0.75833]]),
    'Deuteranopia': np.array([[0.625, 0.375, 0.0],
                              [0.7, 0.3, 0.0],
                              [0.0, 0.3, 0.7]]),
    'Tritanopia': np.array([[0.95, 0.05, 0.0],
                            [0.0, 0.43333, 0.56667],
                            [0.0, 0.475, 0.525]]),
}

# Function to apply CVD filter using LAB adjustments
def apply_cvd_lab_simulation(image, cvd_matrix, brightness=0, contrast=1, hue_shift=0):
    # Convert the image from RGB to LAB
    img_lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB).astype(np.float32)
    
    # Apply brightness and contrast adjustments to the L* channel
    l_channel, a_channel, b_channel = cv2.split(img_lab)
    l_channel = cv2.add(l_channel, brightness)
    l_channel = cv2.multiply(l_channel, contrast)
    l_channel = np.clip(l_channel, 0, 255)
    
    # Apply CVD matrix transformation to the a* and b* channels in RGB space
    img_rgb = cv2.cvtColor(cv2.merge([l_channel, a_channel, b_channel]).astype(np.uint8), cv2.COLOR_LAB2RGB)
    img_rgb = np.dot(img_rgb / 255.0, cvd_matrix.T)
    img_rgb = np.clip(img_rgb * 255, 0, 255).astype(np.uint8)
    
    # Convert back to LAB for hue adjustment
    img_lab_cvd = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    _, a_channel, b_channel = cv2.split(img_lab_cvd)
    
    # Adjust hue by shifting a* and b* channels
    a_channel += hue_shift
    b_channel -= hue_shift
    
    # Clip and merge channels
    img_lab_final = cv2.merge([l_channel, a_channel, b_channel])
    img_lab_final = np.clip(img_lab_final, 0, 255).astype(np.uint8)
    
    # Convert final image back to RGB for display
    final_image = cv2.cvtColor(img_lab_final, cv2.COLOR_LAB2RGB)
    return final_image

# Function to display original and simulated images with widget adjustments
def display_cvd_simulations_lab(image_path, brightness=0, contrast=1, hue_shift=0):
    # Load original image
    original_img = Image.open(image_path).convert("RGB")
    original_img = np.array(original_img)
    
    # Plot original and each CVD simulation
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    axes[0].imshow(original_img)
    axes[0].set_title("Original")
    
    # Apply and display each CVD filter with adjustments
    for i, (cvd_type, matrix) in enumerate(cvd_matrices.items(), start=1):
        cvd_img = apply_cvd_lab_simulation(original_img, matrix, brightness, contrast, hue_shift)
        axes[i].imshow(cvd_img)
        axes[i].set_title(f"{cvd_type}\nBrightness: {brightness}, Contrast: {contrast}, Hue Shift: {hue_shift}")
    
    # Turn off axis for all plots
    for ax in axes:
        ax.axis('off')
    
    plt.show()

# Primary sliders for brightness, contrast, and hue shift
brightness_slider = widgets.IntSlider(value=0, min=-100, max=100, step=5, description="Brightness")
contrast_slider = widgets.FloatSlider(value=1.0, min=0.5, max=2.0, step=0.1, description="Contrast")
hue_shift_slider = widgets.IntSlider(value=0, min=-50, max=50, step=5, description="Hue Shift")

# Range sliders to control the min and max for the main sliders
brightness_range = widgets.IntRangeSlider(value=[-100, 100], min=-200, max=200, step=10, description="Brightness Range")
contrast_range = widgets.FloatRangeSlider(value=[0.5, 2.0], min=0.1, max=3.0, step=0.1, description="Contrast Range")
hue_shift_range = widgets.IntRangeSlider(value=[-50, 50], min=-100, max=100, step=5, description="Hue Shift Range")

# Update functions to dynamically change slider ranges
def update_brightness_range(change):
    brightness_slider.min = brightness_range.value[0]
    brightness_slider.max = brightness_range.value[1]

def update_contrast_range(change):
    contrast_slider.min = contrast_range.value[0]
    contrast_slider.max = contrast_range.value[1]

def update_hue_shift_range(change):
    hue_shift_slider.min = hue_shift_range.value[0]
    hue_shift_slider.max = hue_shift_range.value[1]

# Observe range changes to update main sliders
brightness_range.observe(update_brightness_range, 'value')
contrast_range.observe(update_contrast_range, 'value')
hue_shift_range.observe(update_hue_shift_range, 'value')

# Interactive display update function
def update_display(brightness, contrast, hue_shift):
    display_cvd_simulations_lab(r"D:\MIT FULL NOTES\MIT PROJECT\MIT PROJECT MATERIALS\Research\CIE COLOR SPACE\own pictures\Project pictures\1000_F_953211589_iL6dkUpvwRCgobq2ezIW3xCjgjbsboI1.jpg", brightness, contrast, hue_shift)

# Display layout with main sliders and range controls
ui = widgets.VBox([
    brightness_range, brightness_slider,
    contrast_range, contrast_slider,
    hue_shift_range, hue_shift_slider
])

# Output interactive display
out = widgets.interactive_output(update_display, {
    'brightness': brightness_slider, 
    'contrast': contrast_slider, 
    'hue_shift': hue_shift_slider
})

# Display UI and output
display(ui, out)

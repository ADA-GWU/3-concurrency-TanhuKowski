import sys
import os
from PIL import Image, ImageTk
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
import threading

# Global lock for progress updates in multithreaded mode
progress_lock = threading.Lock()

def calculate_average_color(image_array, x, y, square_size):
    """
    Calculates the average RGB color of a block.
    """
    block = image_array[y:y + square_size, x:x + square_size]
    avg_color = block.reshape(-1, 3).mean(axis=0).astype(int)
    image_array[y:y + square_size, x:x + square_size] = avg_color

def process_single_thread(image, square_size, update_callback=None):
    """
    Processes the image using a single thread and updates progress for each block.
    """
    image_array = np.array(image)
    height, width, _ = image_array.shape
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            calculate_average_color(image_array, x, y, square_size)
            if update_callback:
                update_callback(image_array)
    return Image.fromarray(image_array)

def process_multi_thread(image, square_size, update_callback=None):
    """
    Processes the image using multiple threads and updates progress for each block.
    """
    image_array = np.array(image)
    height, width, _ = image_array.shape

    def process_block_and_update(x, y):
        calculate_average_color(image_array, x, y, square_size)
        if update_callback:
            with progress_lock:
                update_callback(image_array)

    with ThreadPoolExecutor() as executor:
        futures = []
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                futures.append(executor.submit(process_block_and_update, x, y))
        for future in futures:
            future.result()  # Wait for each thread to finish
    return Image.fromarray(image_array)

def resize_image_for_display(image, window_size=(800, 600)):
    """
    Resizes the image for display if it's larger than the given window size.
    """
    width, height = image.size
    max_width, max_height = window_size
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.ANTIALIAS)
    return image

def update_display(image_array, root, img_label):
    """
    Updates the image display in the GUI window for each processed block.
    """
    image = Image.fromarray(image_array)
    resized_image = resize_image_for_display(image)
    photo = ImageTk.PhotoImage(resized_image)
    img_label.config(image=photo)
    img_label.image = photo
    root.update()

def main():
    # Check argument validity
    if len(sys.argv) != 4:
        print("Usage: python yourprogram.py <file_name> <square_size> <mode>")
        sys.exit(1)

    file_name, square_size, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3].upper()

    # Validate file existence
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    # Validate mode
    if mode not in ['S', 'M']:
        print("Error: Mode must be 'S' (Single-threaded) or 'M' (Multi-threaded).")
        sys.exit(1)

    # Load the image
    try:
        image = Image.open(file_name).convert("RGB")
    except Exception as e:
        print(f"Error: Unable to open image. {e}")
        sys.exit(1)

    # Initialize GUI
    root = tk.Tk()
    root.title("Image Averaging Progress")
    img_label = tk.Label(root)
    img_label.pack()

    # Define update callback for progress visualization
    def update_callback(image_array):
        update_display(image_array, root, img_label)

    # Process the image
    result_image = None
    if mode == 'S':
        print("Processing in single-threaded mode...")
        result_image = process_single_thread(image, square_size, update_callback)
    elif mode == 'M':
        print("Processing in multi-threaded mode...")
        result_image = process_multi_thread(image, square_size, update_callback)

    # Save the result
    result_image.save("result.jpg")
    print("Processing completed. Result saved as 'result.jpg'.")

    # Final display
    update_display(np.array(result_image), root, img_label)
    print("Close the window to exit.")
    root.mainloop()

if __name__ == "__main__":
    main()

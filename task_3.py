import sys
import os
from PIL import Image, ImageTk
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk


def calculate_average_color(image_array, x, y, square_size):
    block = image_array[y:y + square_size, x:x + square_size]
    avg_color = block.reshape(-1, 3).mean(axis=0).astype(int)
    image_array[y:y + square_size, x:x + square_size] = avg_color


def process_single_thread(image, square_size):
    image_array = np.array(image)
    height, width, _ = image_array.shape

    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            calculate_average_color(image_array, x, y, square_size)

    return Image.fromarray(image_array)


def process_multi_thread(image, square_size):
    image_array = np.array(image)
    height, width, _ = image_array.shape

    def process_block(x, y):
        calculate_average_color(image_array, x, y, square_size)

    with ThreadPoolExecutor() as executor:
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                executor.submit(process_block, x, y)

    return Image.fromarray(image_array)

def resize_image_for_display(image, window_size=(800, 600)):
    width, height = image.size
    max_width, max_height = window_size

    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.LANCZOS)

    return image



def update_display(image, root, img_label):
    resized_image = resize_image_for_display(image)
    photo = ImageTk.PhotoImage(resized_image)
    img_label.config(image=photo)
    img_label.image = photo
    root.update()


def main():
    if len(sys.argv) != 4:
        print("Usage: python yourprogram.py <file_name> <square_size> <mode>")
        sys.exit(1)

    file_name, square_size, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3].upper()

    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    if mode not in ['S', 'M']:
        print("Error: Mode must be 'S' (Single-threaded) or 'M' (Multi-threaded).")
        sys.exit(1)

    try:
        image = Image.open(file_name).convert("RGB")
    except Exception as e:
        print(f"Error: Unable to open image. {e}")
        sys.exit(1)

    root = tk.Tk()
    root.title("Image Averaging Progress")
    img_label = tk.Label(root)
    img_label.pack()

    print(f"Processing in {'single-threaded' if mode == 'S' else 'multi-threaded'} mode...")

    if mode == 'S':
        processed_image = process_single_thread(image, square_size)
    else:
        processed_image = process_multi_thread(image, square_size)

    processed_image.save("result.jpg")
    print("Processing completed. Result saved as 'result.jpg'.")

    update_display(processed_image, root, img_label)
    print("Close the window to exit.")
    root.mainloop()


if __name__ == "__main__":
    main()

import sys
import os
from PIL import Image, ImageTk
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
import threading
import queue

progress_lock = threading.Lock()

def calculate_average_color(image_array, x, y, square_size):
    block = image_array[y:y + square_size, x:x + square_size]
    avg_color = block.reshape(-1, 3).mean(axis=0).astype(int)
    image_array[y:y + square_size, x:x + square_size] = avg_color

def process_multi_thread(image, square_size, update_queue):
    image_array = np.array(image)
    height, width, _ = image_array.shape

    def process_block(x, y):
        calculate_average_color(image_array, x, y, square_size)
        with progress_lock:
            update_queue.put(image_array.copy())

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_block, x, y) for y in range(0, height, square_size) for x in range(0, width, square_size)]
        for future in futures:
            future.result()
    return Image.fromarray(image_array)

def process_single_thread(image, square_size, update_queue):
    image_array = np.array(image)
    height, width, _ = image_array.shape
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            calculate_average_color(image_array, x, y, square_size)
            update_queue.put(image_array.copy())
    return Image.fromarray(image_array)

def resize_image_for_display(image, window_size=(800, 600)):
    width, height = image.size
    max_width, max_height = window_size
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.ANTIALIAS)
    return image

def update_display(image_array, root, img_label):
    image = Image.fromarray(image_array)
    resized_image = resize_image_for_display(image)
    photo = ImageTk.PhotoImage(resized_image)
    img_label.config(image=photo)
    img_label.image = photo
    root.update()

def gui_updater(root, img_label, update_queue):
    while True:
        try:
            image_array = update_queue.get(timeout=0.1)
            update_display(image_array, root, img_label)
        except queue.Empty:
            break

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

    update_queue = queue.Queue()

    result_image = None
    if mode == 'S':
        print("Processing in single-threaded mode...")
        result_image = process_single_thread(image, square_size, update_queue)
    elif mode == 'M':
        print("Processing in multi-threaded mode...")
        result_image = process_multi_thread(image, square_size, update_queue)

    threading.Thread(target=gui_updater, args=(root, img_label, update_queue), daemon=True).start()

    result_image.save("result.jpg")
    print("Processing completed. Result saved as 'result.jpg'.")

    update_display(np.array(result_image), root, img_label)
    print("Close the window to exit.")
    root.mainloop()

if __name__ == "__main__":
    main()
